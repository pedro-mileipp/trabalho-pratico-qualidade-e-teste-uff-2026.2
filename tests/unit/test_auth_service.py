from __future__ import annotations

import pytest
from werkzeug.security import check_password_hash, generate_password_hash

from app.modelos import Cliente
from app.repositorios.repositorio import Repositorio
from app.servicos.auth import AuthService, CredenciaisInvalidas, EmailJaCadastrado


@pytest.fixture
def repositorio_mock(mocker):
    repo = mocker.Mock(spec=Repositorio)
    repo.buscar_cliente_por_email.return_value = None
    repo.criar_cliente.side_effect = lambda nome, email, senha_hash: Cliente(
        id=1,
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        saldo=0.0,
    )
    return repo


@pytest.fixture
def servico(repositorio_mock) -> AuthService:
    return AuthService(repositorio=repositorio_mock)


class TestRegistrar:
    @pytest.mark.parametrize(
        ("nome", "email", "senha"),
        [
            ("", "maria@exemplo.com", "123456"),
            ("   ", "maria@exemplo.com", "123456"),
            ("Maria", "", "123456"),
            ("Maria", "   ", "123456"),
            ("Maria", "maria@exemplo.com", ""),
        ],
    )
    def test_campos_vazios_ou_apenas_espacos_levanta_credenciais_invalidas(
        self, servico: AuthService, repositorio_mock, nome: str, email: str, senha: str
    ) -> None:
        with pytest.raises(CredenciaisInvalidas, match="preencha todos os campos"):
            servico.registrar(nome, email, senha)

        repositorio_mock.criar_cliente.assert_not_called()

    def test_nome_e_email_com_espacos_e_email_em_minusculas_sao_normalizados(
        self, servico: AuthService, repositorio_mock
    ) -> None:
        cliente = servico.registrar("  Maria Silva  ", "  MaRiA.SiLvA@Exemplo.COM  ", "minha_senha_123")

        assert cliente.nome == "Maria Silva"
        assert cliente.email == "maria.silva@exemplo.com"
        repositorio_mock.buscar_cliente_por_email.assert_called_once_with("maria.silva@exemplo.com")

        args_chamada = repositorio_mock.criar_cliente.call_args[0]
        assert args_chamada[0] == "Maria Silva"
        assert args_chamada[1] == "maria.silva@exemplo.com"

    def test_senha_com_5_caracteres_levanta_credenciais_invalidas(
        self, servico: AuthService, repositorio_mock
    ) -> None:
        with pytest.raises(CredenciaisInvalidas, match="senha muito curta"):
            servico.registrar("Maria", "maria@exemplo.com", "12345")

        repositorio_mock.criar_cliente.assert_not_called()

    def test_senha_com_6_caracteres_e_aceita_e_salva_como_hash(
        self, servico: AuthService, repositorio_mock
    ) -> None:
        senha_plana = "123456"

        cliente = servico.registrar("Maria", "maria@exemplo.com", senha_plana)

        args_chamada = repositorio_mock.criar_cliente.call_args[0]
        senha_hash_enviada = args_chamada[2]

        assert senha_hash_enviada != senha_plana
        assert check_password_hash(senha_hash_enviada, senha_plana)
        assert check_password_hash(cliente.senha_hash, senha_plana)

    def test_email_duplicado_levanta_email_ja_cadastrado(
        self, servico: AuthService, repositorio_mock
    ) -> None:
        repositorio_mock.buscar_cliente_por_email.return_value = Cliente(
            id=10,
            nome="Existente",
            email="maria@exemplo.com",
            senha_hash=generate_password_hash("outrasenha", method="pbkdf2:sha256"),
            saldo=0.0,
        )

        with pytest.raises(EmailJaCadastrado):
            servico.registrar("Maria Nova", "  MARIA@EXEMPLO.COM  ", "123456")

        repositorio_mock.criar_cliente.assert_not_called()


class TestAutenticar:
    def test_cliente_inexistente_levanta_credenciais_invalidas(
        self, servico: AuthService, repositorio_mock
    ) -> None:
        repositorio_mock.buscar_cliente_por_email.return_value = None

        with pytest.raises(CredenciaisInvalidas, match="credenciais invalidas"):
            servico.autenticar("naoexiste@exemplo.com", "123456")

    def test_senha_errada_levanta_credenciais_invalidas(
        self, servico: AuthService, repositorio_mock
    ) -> None:
        repositorio_mock.buscar_cliente_por_email.return_value = Cliente(
            id=1,
            nome="Maria",
            email="maria@exemplo.com",
            senha_hash=generate_password_hash("senha_correta", method="pbkdf2:sha256"),
            saldo=0.0,
        )

        with pytest.raises(CredenciaisInvalidas, match="credenciais invalidas"):
            servico.autenticar("maria@exemplo.com", "senha_errada")

    def test_email_com_maiusculas_e_espacos_autentica_com_sucesso(
        self, servico: AuthService, repositorio_mock
    ) -> None:
        senha_correta = "segredo_forte"
        cliente_esperado = Cliente(
            id=7,
            nome="Maria",
            email="maria@exemplo.com",
            senha_hash=generate_password_hash(senha_correta, method="pbkdf2:sha256"),
            saldo=0.0,
        )
        repositorio_mock.buscar_cliente_por_email.return_value = cliente_esperado

        cliente_autenticado = servico.autenticar("  MARIA@EXEMPLO.COM  ", senha_correta)

        repositorio_mock.buscar_cliente_por_email.assert_called_once_with("maria@exemplo.com")
        assert cliente_autenticado == cliente_esperado