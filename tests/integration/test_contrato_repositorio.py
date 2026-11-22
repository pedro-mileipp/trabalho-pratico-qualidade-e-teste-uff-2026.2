"""Testes de integração do contrato de Repositorio nas duas implementações (issue #54).

Chama o repositório diretamente (sem serviços e sem HTTP) para conferir que SqliteRepositorio e
MemoriaRepositorio cumprem o mesmo contrato da classe abstrata Repositorio. Nenhum mock é usado;
o SQLite usa um banco temporário em tmp_path.

Critérios cobertos:
1. criar_cliente, buscar_cliente_por_id e buscar_cliente_por_email.
2. atualizar_saldo e atualizar_score persistem.
3. registrar_transacao devolve a data em ISO e listar_transacoes mantém a ordem de inserção.
4. Divergências entre as implementações, fixadas como comportamento atual (sem alterar app/).
"""

from __future__ import annotations

import sqlite3
from datetime import datetime

import pytest

from app.repositorios.memoria_repositorio import MemoriaRepositorio
from app.repositorios.repositorio import Repositorio
from app.repositorios.sqlite_repositorio import SqliteRepositorio

HASH_QUALQUER = "pbkdf2:sha256:hash-de-teste"


class TestContratoRepositorio:
    """O mesmo contrato, executado no SQLite e na memória (fixture `repositorio`)."""

    def test_criar_cliente_comeca_com_saldo_zero_e_score_500(self, repositorio: Repositorio) -> None:
        cliente = repositorio.criar_cliente("Carla Dias", "carla@teste.com", HASH_QUALQUER)

        assert cliente.id is not None
        assert cliente.nome == "Carla Dias"
        assert cliente.email == "carla@teste.com"
        assert cliente.senha_hash == HASH_QUALQUER
        assert cliente.saldo == 0
        assert cliente.score == 500

    def test_buscar_por_id_e_por_email_encontram_o_cliente(self, repositorio: Repositorio) -> None:
        criado = repositorio.criar_cliente("Carla Dias", "carla@teste.com", HASH_QUALQUER)

        assert repositorio.buscar_cliente_por_id(criado.id) == criado
        assert repositorio.buscar_cliente_por_email("carla@teste.com") == criado

    def test_buscas_por_cliente_inexistente_devolvem_none(self, repositorio: Repositorio) -> None:
        repositorio.criar_cliente("Carla Dias", "carla@teste.com", HASH_QUALQUER)

        assert repositorio.buscar_cliente_por_id(999) is None
        assert repositorio.buscar_cliente_por_email("ninguem@teste.com") is None

    def test_clientes_recebem_ids_distintos(self, repositorio: Repositorio) -> None:
        primeiro = repositorio.criar_cliente("Carla Dias", "carla@teste.com", HASH_QUALQUER)
        segundo = repositorio.criar_cliente("Davi Melo", "davi@teste.com", HASH_QUALQUER)

        assert primeiro.id != segundo.id

    def test_atualizar_saldo_persiste(self, repositorio: Repositorio) -> None:
        cliente = repositorio.criar_cliente("Carla Dias", "carla@teste.com", HASH_QUALQUER)

        repositorio.atualizar_saldo(cliente.id, 1234.56)

        atualizado = repositorio.buscar_cliente_por_id(cliente.id)
        assert atualizado.saldo == pytest.approx(1234.56)
        assert atualizado.score == 500

    def test_atualizar_score_persiste(self, repositorio: Repositorio) -> None:
        cliente = repositorio.criar_cliente("Carla Dias", "carla@teste.com", HASH_QUALQUER)
        repositorio.atualizar_saldo(cliente.id, 100.0)

        repositorio.atualizar_score(cliente.id, 820)

        atualizado = repositorio.buscar_cliente_por_id(cliente.id)
        assert atualizado.score == 820
        assert atualizado.saldo == pytest.approx(100.0)

    def test_registrar_transacao_devolve_data_em_iso(self, repositorio: Repositorio) -> None:
        cliente = repositorio.criar_cliente("Carla Dias", "carla@teste.com", HASH_QUALQUER)

        transacao = repositorio.registrar_transacao(cliente.id, "pix", "PIX email", -50.0)

        assert transacao.cliente_id == cliente.id
        assert transacao.tipo == "pix"
        assert transacao.descricao == "PIX email"
        assert transacao.valor == pytest.approx(-50.0)
        assert isinstance(datetime.fromisoformat(transacao.data), datetime)

    def test_listar_transacoes_mantem_ordem_de_insercao(self, repositorio: Repositorio) -> None:
        cliente = repositorio.criar_cliente("Carla Dias", "carla@teste.com", HASH_QUALQUER)
        outro = repositorio.criar_cliente("Davi Melo", "davi@teste.com", HASH_QUALQUER)
        repositorio.registrar_transacao(cliente.id, "pix", "primeira", -10.0)
        repositorio.registrar_transacao(outro.id, "pix", "do outro cliente", -99.0)
        repositorio.registrar_transacao(cliente.id, "pix", "segunda", -20.0)
        repositorio.registrar_transacao(cliente.id, "pix", "terceira", -30.0)

        extrato = repositorio.listar_transacoes(cliente.id)

        assert [t.descricao for t in extrato] == ["primeira", "segunda", "terceira"]
        assert repositorio.listar_transacoes(999) == []


class TestDivergenciasEntreImplementacoes:
    """Comportamento atual em que SQLite e memória divergem. Os testes fixam o que o código faz hoje
    (o código de produção não foi alterado); o AuthService evita o primeiro caso, porque confere o
    e-mail antes de criar o cliente."""

    # Divergência 1: e-mail duplicado direto no repositório.
    # SQLite: a coluna email é UNIQUE, então o banco recusa com IntegrityError.
    # Memória: não há verificação; o segundo cliente é criado com outro id.

    def test_sqlite_recusa_email_duplicado_com_integrity_error(self, repo_sqlite: SqliteRepositorio) -> None:
        repo_sqlite.criar_cliente("Carla Dias", "carla@teste.com", HASH_QUALQUER)

        with pytest.raises(sqlite3.IntegrityError):
            repo_sqlite.criar_cliente("Outra Carla", "carla@teste.com", HASH_QUALQUER)

    def test_memoria_aceita_email_duplicado(self, repo_memoria: MemoriaRepositorio) -> None:
        primeiro = repo_memoria.criar_cliente("Carla Dias", "carla@teste.com", HASH_QUALQUER)

        segundo = repo_memoria.criar_cliente("Outra Carla", "carla@teste.com", HASH_QUALQUER)

        assert segundo.id != primeiro.id
        # A busca por e-mail devolve o primeiro cadastrado.
        assert repo_memoria.buscar_cliente_por_email("carla@teste.com") == primeiro

    # Divergência 2: atualizar_saldo com id inexistente.
    # SQLite: o UPDATE não encontra linha e não faz nada (sem erro).
    # Memória: o acesso ao dicionário lança KeyError.

    def test_sqlite_ignora_atualizar_saldo_de_id_inexistente(self, repo_sqlite: SqliteRepositorio) -> None:
        repo_sqlite.atualizar_saldo(999, 100.0)

        assert repo_sqlite.buscar_cliente_por_id(999) is None

    def test_memoria_lanca_key_error_ao_atualizar_saldo_de_id_inexistente(
        self, repo_memoria: MemoriaRepositorio
    ) -> None:
        with pytest.raises(KeyError):
            repo_memoria.atualizar_saldo(999, 100.0)
