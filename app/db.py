from __future__ import annotations

import sqlite3

from flask import Flask, current_app, g

ESQUEMA = """
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    saldo REAL NOT NULL DEFAULT 0,
    score INTEGER NOT NULL DEFAULT 500
);

CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    descricao TEXT,
    valor REAL NOT NULL,
    data TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
);
"""


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app: Flask) -> None:
    with app.app_context():
        get_db().executescript(ESQUEMA)
        get_db().commit()
    app.teardown_appcontext(close_db)