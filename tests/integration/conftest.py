from __future__ import annotations

import sqlite3
from collections.abc import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import Config
from app.db import get_db


@pytest.fixture
def app(tmp_path) -> Generator[Flask, None, None]:
    """Cria uma instância isolada da aplicação com banco SQLite temporário e TESTING=True."""
    banco_temporario = str(tmp_path / "banco_integracao.db")

    class ConfigIntegracao(Config):
        TESTING = True
        DATABASE = banco_temporario
        SECRET_KEY = "chave-secreta-integracao-banco-digital"

    aplicacao = create_app(ConfigIntegracao)
    yield aplicacao


@pytest.fixture
def cliente(app: Flask) -> FlaskClient:
    """Cliente de testes Flask com gerenciamento de cookies/sessão."""
    return app.test_client()


@pytest.fixture
def conexao_banco(app: Flask) -> Generator[sqlite3.Connection, None, None]:
    """Conexão direta ao banco temporário do teste para asserções e consultas de persistência."""
    conexao = sqlite3.connect(app.config["DATABASE"])
    conexao.row_factory = sqlite3.Row
    yield conexao
    conexao.close()


@pytest.fixture
def cliente_autenticado(app: Flask, cliente: FlaskClient) -> dict[str, str | int]:
    """Cadastra e autentica um cliente via /registro, deixando a sessão pronta para uso."""
    dados_usuario = {
        "nome": "Usuário Integração",
        "email": "integracao@teste.com",
        "senha": "senha-forte-123",
    }
    resposta = cliente.post("/registro", data=dados_usuario)
    assert resposta.status_code == 302, "Falha ao registrar cliente na fixture cliente_autenticado"

    with app.app_context():
        db = get_db()
        cursor = db.execute("SELECT id FROM clientes WHERE email = ?", (dados_usuario["email"],))
        linha = cursor.fetchone()
        cliente_id = linha["id"] if linha else 1

    dados_usuario["id"] = cliente_id
    return dados_usuario


@pytest.fixture
def definir_saldo(app: Flask):
    """Factory fixture para ajustar o saldo de um cliente diretamente no banco."""
    def _ajustar(cliente_id: int, saldo: float) -> None:
        with app.app_context():
            db = get_db()
            db.execute("UPDATE clientes SET saldo = ? WHERE id = ?", (saldo, cliente_id))
            db.commit()

    return _ajustar
