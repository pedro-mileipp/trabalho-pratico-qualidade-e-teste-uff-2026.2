"""Testes de integração entre os serviços e os repositórios reais da aplicação Banco Digital (issue #54).

Diferente de test_rotas.py (#55), aqui não há HTTP: os testes chamam AuthService e TransacaoService
diretamente sobre o SqliteRepositorio (banco SQLite temporário em tmp_path) e sobre o
MemoriaRepositorio. O app Flask só fornece o contexto e o banco. Nenhum mock é usado.

Critérios cobertos:
1. AuthService registra e autentica um cliente real.
2. TransacaoService transfere e grava saldo e extrato (listar_transacoes).
3. Transferência recusada não altera saldo nem extrato.
4. O mesmo contrato roda no SqliteRepositorio e no MemoriaRepositorio (fixture `repositorio`).
5. Os dados do SQLite persistem entre contextos e nenhum banco.db é criado no workspace.

Observação: TransacaoService.transferir_pix anota `horario: datetime | None`, mas
TransacaoPix.autorizar espera `datetime.time`. Os testes sempre passam `horario=time(...)`, porque
sem horário o resultado dependeria da hora da execução (o limite noturno começa às 20h).
"""

from __future__ import annotations

import sqlite3
from collections.abc import Generator
from datetime import time
from pathlib import Path

import pytest
from flask import Flask

from app.db import get_db
from app.dominio.pix import ChaveTipo, ResultadoPix
from app.modelos import Cliente
from app.repositorios.repositorio import Repositorio
from app.repositorios.sqlite_repositorio import SqliteRepositorio
from app.servicos.auth import AuthService, CredenciaisInvalidas, EmailJaCadastrado
from app.servicos.transacoes import TransacaoRecusada, TransacaoService

HORARIO_DIURNO = time(10, 0)
HORARIO_NOTURNO = time(22, 0)
CHAVE_EMAIL_VALIDA = "destino@banco.com"
SENHA = "senha-forte-123"
BANCO_DO_WORKSPACE = Path(__file__).resolve().parents[2] / "banco.db"


def _estado_banco_workspace() -> tuple[bool, float | None]:
    if BANCO_DO_WORKSPACE.exists():
        return True, BANCO_DO_WORKSPACE.stat().st_mtime
    return False, None


@pytest.fixture(autouse=True)
def banco_do_workspace_intocado() -> Generator[None, None, None]:
    """Garante que o teste não cria nem altera o banco.db da raiz do projeto (pode já existir localmente)."""
    antes = _estado_banco_workspace()
    yield
    assert _estado_banco_workspace() == antes, "o teste criou ou alterou o banco.db do workspace"


def _cliente_com_saldo(repositorio: Repositorio, saldo: float, email: str = "pagador@teste.com") -> Cliente:
    """Registra um cliente real pelo AuthService e define o saldo pelo próprio repositório."""
    cliente = AuthService(repositorio).registrar("Cliente Pagador", email, SENHA)
    repositorio.atualizar_saldo(cliente.id, saldo)
    return cliente


class TestAuthServiceComRepositorioReal:
    """Registro e autenticação gravando e lendo do repositório real."""

    def test_registra_e_autentica_cliente(self, repositorio: Repositorio) -> None:
        servico = AuthService(repositorio)

        registrado = servico.registrar("Ana Souza", "  Ana@Teste.COM ", SENHA)
        autenticado = servico.autenticar("ana@teste.com", SENHA)

        assert autenticado.id == registrado.id
        salvo = repositorio.buscar_cliente_por_id(registrado.id)
        assert salvo is not None
        assert salvo.email == "ana@teste.com"
        assert salvo.senha_hash.startswith("pbkdf2:sha256")
        assert salvo.senha_hash != SENHA

    def test_autentica_com_email_em_maiusculas_e_espacos(self, repositorio: Repositorio) -> None:
        servico = AuthService(repositorio)
        registrado = servico.registrar("Ana Souza", "ana@teste.com", SENHA)

        assert servico.autenticar("  ANA@teste.com ", SENHA).id == registrado.id

    @pytest.mark.parametrize("email_repetido", ["ana@teste.com", "  ANA@Teste.com "])
    def test_email_duplicado_lanca_email_ja_cadastrado(
        self, repositorio: Repositorio, email_repetido: str
    ) -> None:
        servico = AuthService(repositorio)
        servico.registrar("Ana Souza", "ana@teste.com", SENHA)

        with pytest.raises(EmailJaCadastrado):
            servico.registrar("Outra Ana", email_repetido, SENHA)

    def test_senha_errada_lanca_credenciais_invalidas(self, repositorio: Repositorio) -> None:
        servico = AuthService(repositorio)
        servico.registrar("Ana Souza", "ana@teste.com", SENHA)

        with pytest.raises(CredenciaisInvalidas):
            servico.autenticar("ana@teste.com", "senha-errada")

    def test_email_inexistente_lanca_credenciais_invalidas(self, repositorio: Repositorio) -> None:
        with pytest.raises(CredenciaisInvalidas):
            AuthService(repositorio).autenticar("ninguem@teste.com", SENHA)


class TestTransacaoServiceComRepositorioReal:
    """PIX aprovado gravando saldo e extrato no repositório real."""

    def test_pix_aprovado_atualiza_saldo_e_extrato(self, repositorio: Repositorio) -> None:
        cliente = _cliente_com_saldo(repositorio, 1000.0)

        novo_saldo = TransacaoService(repositorio).transferir_pix(
            cliente.id, CHAVE_EMAIL_VALIDA, ChaveTipo.EMAIL, 300.0, horario=HORARIO_DIURNO
        )

        assert novo_saldo == pytest.approx(700.0)
        assert repositorio.buscar_cliente_por_id(cliente.id).saldo == pytest.approx(700.0)
        extrato = repositorio.listar_transacoes(cliente.id)
        assert len(extrato) == 1
        assert extrato[0].tipo == "pix"
        assert extrato[0].valor == pytest.approx(-300.0)
        assert extrato[0].descricao == "PIX email"

    def test_dois_pix_seguidos_acumulam_saldo_e_extrato_em_ordem(self, repositorio: Repositorio) -> None:
        cliente = _cliente_com_saldo(repositorio, 1000.0)
        servico = TransacaoService(repositorio)

        servico.transferir_pix(cliente.id, CHAVE_EMAIL_VALIDA, ChaveTipo.EMAIL, 300.0, horario=HORARIO_DIURNO)
        saldo_final = servico.transferir_pix(
            cliente.id, "529.982.247-25", ChaveTipo.CPF, 200.0, horario=HORARIO_DIURNO
        )

        assert saldo_final == pytest.approx(500.0)
        assert repositorio.buscar_cliente_por_id(cliente.id).saldo == pytest.approx(500.0)
        extrato = repositorio.listar_transacoes(cliente.id)
        assert [t.valor for t in extrato] == pytest.approx([-300.0, -200.0])
        assert [t.descricao for t in extrato] == ["PIX email", "PIX cpf"]

    def test_pix_do_cliente_a_nao_aparece_no_extrato_do_cliente_b(self, repositorio: Repositorio) -> None:
        cliente_a = _cliente_com_saldo(repositorio, 1000.0, email="a@teste.com")
        cliente_b = _cliente_com_saldo(repositorio, 1000.0, email="b@teste.com")

        TransacaoService(repositorio).transferir_pix(
            cliente_a.id, CHAVE_EMAIL_VALIDA, ChaveTipo.EMAIL, 300.0, horario=HORARIO_DIURNO
        )

        assert len(repositorio.listar_transacoes(cliente_a.id)) == 1
        assert repositorio.listar_transacoes(cliente_b.id) == []
        assert repositorio.buscar_cliente_por_id(cliente_b.id).saldo == pytest.approx(1000.0)


class TestTransferenciaRecusadaNaoAlteraEstado:
    """PIX recusado não pode alterar saldo nem extrato."""

    @pytest.mark.parametrize(
        ("chave", "tipo", "valor", "horario", "resultado_esperado"),
        [
            pytest.param(
                CHAVE_EMAIL_VALIDA, ChaveTipo.EMAIL, 1500.0, HORARIO_DIURNO,
                ResultadoPix.SALDO_INSUFICIENTE, id="saldo_insuficiente",
            ),
            pytest.param(
                "email-sem-arroba", ChaveTipo.EMAIL, 100.0, HORARIO_DIURNO,
                ResultadoPix.CHAVE_INVALIDA, id="chave_invalida",
            ),
            pytest.param(
                CHAVE_EMAIL_VALIDA, ChaveTipo.EMAIL, 1500.0, HORARIO_NOTURNO,
                ResultadoPix.FORA_HORARIO, id="limite_noturno",
            ),
        ],
    )
    def test_recusa_mantem_saldo_e_extrato(
        self,
        repositorio: Repositorio,
        chave: str,
        tipo: ChaveTipo,
        valor: float,
        horario: time,
        resultado_esperado: ResultadoPix,
    ) -> None:
        # Saldo 1000: no caso noturno, 1500 passa do limite noturno (1000) antes da checagem de saldo.
        cliente = _cliente_com_saldo(repositorio, 1000.0)

        with pytest.raises(TransacaoRecusada) as erro:
            TransacaoService(repositorio).transferir_pix(cliente.id, chave, tipo, valor, horario=horario)

        assert erro.value.resultado is resultado_esperado
        assert repositorio.buscar_cliente_por_id(cliente.id).saldo == pytest.approx(1000.0)
        assert repositorio.listar_transacoes(cliente.id) == []

    def test_cliente_inexistente_e_recusado(self, repositorio: Repositorio) -> None:
        with pytest.raises(TransacaoRecusada) as erro:
            TransacaoService(repositorio).transferir_pix(
                999, CHAVE_EMAIL_VALIDA, ChaveTipo.EMAIL, 100.0, horario=HORARIO_DIURNO
            )

        assert erro.value.resultado is ResultadoPix.CHAVE_INVALIDA
        assert repositorio.listar_transacoes(999) == []


class TestPersistenciaSqlite:
    """Só SQLite: os dados ficam gravados no arquivo temporário, e não apenas na conexão aberta."""

    def test_dados_persistem_em_novo_contexto_e_conferem_com_select(
        self, app: Flask, conexao_banco: sqlite3.Connection
    ) -> None:
        with app.app_context():
            repo = SqliteRepositorio(get_db)
            cliente = AuthService(repo).registrar("Bruno Lima", "bruno@teste.com", SENHA)
            repo.atualizar_saldo(cliente.id, 1000.0)
            TransacaoService(repo).transferir_pix(
                cliente.id, CHAVE_EMAIL_VALIDA, ChaveTipo.EMAIL, 250.0, horario=HORARIO_DIURNO
            )

        # Contexto novo = conexão nova (a anterior foi fechada no teardown do app context).
        with app.app_context():
            repo_novo = SqliteRepositorio(get_db)
            assert AuthService(repo_novo).autenticar("bruno@teste.com", SENHA).id == cliente.id
            assert repo_novo.buscar_cliente_por_id(cliente.id).saldo == pytest.approx(750.0)
            assert len(repo_novo.listar_transacoes(cliente.id)) == 1

        linha_cliente = conexao_banco.execute(
            "SELECT email, saldo FROM clientes WHERE id = ?", (cliente.id,)
        ).fetchone()
        assert linha_cliente["email"] == "bruno@teste.com"
        assert linha_cliente["saldo"] == pytest.approx(750.0)
        linhas_transacao = conexao_banco.execute(
            "SELECT tipo, descricao, valor FROM transacoes WHERE cliente_id = ?", (cliente.id,)
        ).fetchall()
        assert [tuple(linha) for linha in linhas_transacao] == [("pix", "PIX email", -250.0)]

    def test_banco_do_teste_fica_dentro_de_tmp_path(self, app: Flask, tmp_path: Path) -> None:
        caminho_banco = Path(app.config["DATABASE"]).resolve()

        assert caminho_banco.is_relative_to(tmp_path.resolve())
        assert caminho_banco != BANCO_DO_WORKSPACE
