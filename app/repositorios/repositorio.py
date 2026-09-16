from __future__ import annotations

from abc import ABC, abstractmethod

from app.modelos import Cliente, Transacao


class Repositorio(ABC):
    @abstractmethod
    def criar_cliente(self, nome: str, email: str, senha_hash: str) -> Cliente: ...

    @abstractmethod
    def buscar_cliente_por_email(self, email: str) -> Cliente | None: ...

    @abstractmethod
    def buscar_cliente_por_id(self, cliente_id: int) -> Cliente | None: ...

    @abstractmethod
    def atualizar_saldo(self, cliente_id: int, novo_saldo: float) -> None: ...

    @abstractmethod
    def atualizar_score(self, cliente_id: int, score: int) -> None: ...

    @abstractmethod
    def registrar_transacao(self, cliente_id: int, tipo: str, descricao: str, valor: float) -> Transacao: ...

    @abstractmethod
    def listar_transacoes(self, cliente_id: int) -> list[Transacao]: ...