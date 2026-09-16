from __future__ import annotations

import sqlite3
from collections.abc import Callable
from datetime import datetime

from app.modelos import Cliente, Transacao

from .repositorio import Repositorio


class SqliteRepositorio(Repositorio):
    def __init__(self, conexao_factory: Callable[[], sqlite3.Connection]) -> None:
        self._conexao_factory = conexao_factory

    def _conn(self) -> sqlite3.Connection:
        return self._conexao_factory()

    def criar_cliente(self, nome: str, email: str, senha_hash: str) -> Cliente:
        conn = self._conn()
        cursor = conn.execute(
            "INSERT INTO clientes (nome, email, senha_hash, saldo, score) VALUES (?, ?, ?, 0, 500)",
            (nome, email, senha_hash),
        )
        conn.commit()
        return self.buscar_cliente_por_id(cursor.lastrowid)

    def buscar_cliente_por_email(self, email: str) -> Cliente | None:
        conn = self._conn()
        linha = conn.execute("SELECT * FROM clientes WHERE email = ?", (email,)).fetchone()
        return self._linha_para_cliente(linha)

    def buscar_cliente_por_id(self, cliente_id: int) -> Cliente | None:
        conn = self._conn()
        linha = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
        return self._linha_para_cliente(linha)

    def atualizar_saldo(self, cliente_id: int, novo_saldo: float) -> None:
        conn = self._conn()
        conn.execute("UPDATE clientes SET saldo = ? WHERE id = ?", (novo_saldo, cliente_id))
        conn.commit()

    def atualizar_score(self, cliente_id: int, score: int) -> None:
        conn = self._conn()
        conn.execute("UPDATE clientes SET score = ? WHERE id = ?", (score, cliente_id))
        conn.commit()

    def registrar_transacao(self, cliente_id: int, tipo: str, descricao: str, valor: float) -> Transacao:
        conn = self._conn()
        data = datetime.now().isoformat()
        cursor = conn.execute(
            "INSERT INTO transacoes (cliente_id, tipo, descricao, valor, data) VALUES (?, ?, ?, ?, ?)",
            (cliente_id, tipo, descricao, valor, data),
        )
        conn.commit()
        return Transacao(cursor.lastrowid, cliente_id, tipo, descricao, valor, data)

    def listar_transacoes(self, cliente_id: int) -> list[Transacao]:
        conn = self._conn()
        linhas = conn.execute(
            "SELECT * FROM transacoes WHERE cliente_id = ? ORDER BY id", (cliente_id,)
        ).fetchall()
        return [
            Transacao(r["id"], r["cliente_id"], r["tipo"], r["descricao"], r["valor"], r["data"])
            for r in linhas
        ]

    @staticmethod
    def _linha_para_cliente(linha: sqlite3.Row | None) -> Cliente | None:
        if linha is None:
            return None
        return Cliente(
            linha["id"],
            linha["nome"],
            linha["email"],
            linha["senha_hash"],
            linha["saldo"],
            linha["score"],
        )