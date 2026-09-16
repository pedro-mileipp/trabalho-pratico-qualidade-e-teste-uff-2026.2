from __future__ import annotations

from werkzeug.security import check_password_hash, generate_password_hash

from app.modelos import Cliente
from app.repositorios.repositorio import Repositorio


class EmailJaCadastrado(Exception):
    pass


class CredenciaisInvalidas(Exception):
    pass


class AuthService:
    def __init__(self, repositorio: Repositorio) -> None:
        self._repositorio = repositorio

    def registrar(self, nome: str, email: str, senha: str) -> Cliente:
        nome = nome.strip()
        email = email.strip().lower()
        if not nome or not email or not senha:
            raise CredenciaisInvalidas("preencha todos os campos")
        if len(senha) < 6:
            raise CredenciaisInvalidas("senha muito curta")
        if self._repositorio.buscar_cliente_por_email(email) is not None:
            raise EmailJaCadastrado(email)
        return self._repositorio.criar_cliente(
            nome, email, generate_password_hash(senha, method="pbkdf2:sha256")
        )

    def autenticar(self, email: str, senha: str) -> Cliente:
        email = email.strip().lower()
        cliente = self._repositorio.buscar_cliente_por_email(email)
        if cliente is None or not check_password_hash(cliente.senha_hash, senha):
            raise CredenciaisInvalidas("credenciais invalidas")
        return cliente