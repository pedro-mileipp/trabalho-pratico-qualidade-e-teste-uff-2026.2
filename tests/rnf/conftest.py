"""Fixtures compartilhadas dos testes de requisitos não funcionais (RNF).

Organização: uma pasta por requisito (ex.: ``tests/rnf/seguranca/``). Estas fixtures valem para
todas as pastas.

Usam o cliente de testes do Flask (sem navegador): cada teste recebe uma aplicação nova, com o
seu próprio banco SQLite temporário, então os testes são independentes entre si.
"""

from __future__ import annotations

import sqlite3

import pytest

from app import create_app
from app.config import Config

NOME = "Cliente Seguro"
EMAIL = "cliente.seguro@teste.com"
SENHA = "senha-forte-123"


@pytest.fixture
def app(tmp_path):
    class ConfigTeste(Config):
        TESTING = True
        DATABASE = str(tmp_path / "banco_rnf.db")
        SECRET_KEY = "chave-dos-testes-rnf"

    return create_app(ConfigTeste)


@pytest.fixture
def cliente_http(app):
    return app.test_client()


@pytest.fixture
def banco(app):
    """Conexão direta ao SQLite do teste, para conferir o que a aplicação gravou."""
    conexao = sqlite3.connect(app.config["DATABASE"])
    yield conexao
    conexao.close()


@pytest.fixture
def cliente_cadastrado(cliente_http) -> dict[str, str]:
    """Cadastra um cliente pela rota /registro, que já deixa a sessão aberta."""
    resposta = cliente_http.post("/registro", data={"nome": NOME, "email": EMAIL, "senha": SENHA})
    assert resposta.status_code == 302, "o cadastro do cliente de teste falhou"
    return {"nome": NOME, "email": EMAIL, "senha": SENHA}
