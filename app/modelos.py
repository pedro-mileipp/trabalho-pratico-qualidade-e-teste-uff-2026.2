from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Cliente:
    id: int
    nome: str
    email: str
    senha_hash: str
    saldo: float
    score: int = 500


@dataclass
class Transacao:
    id: int
    cliente_id: int
    tipo: str
    descricao: str
    valor: float
    data: str