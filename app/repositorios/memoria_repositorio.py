from __future__ import annotations

from datetime import datetime

from app.modelos import Cliente, Transacao

from .repositorio import Repositorio


class MemoriaRepositorio(Repositorio):
    def __init__(self) -> None:
        self._clientes: dict[int, Cliente] = {}
        self._transacoes: list[Transacao] = []
        self._proximo_id_cliente = 1
        self._proximo_id_transacao = 1

    def criar_cliente(self, nome: str, email: str, senha_hash: str) -> Cliente:
        cliente = Cliente(self._proximo_id_cliente, nome, email, senha_hash, 0.0)
        self._proximo_id_cliente += 1
        self._clientes[cliente.id] = cliente
        return cliente

    def buscar_cliente_por_email(self, email: str) -> Cliente | None:
        for cliente in self._clientes.values():
            if cliente.email == email:
                return cliente
        return None

    def buscar_cliente_por_id(self, cliente_id: int) -> Cliente | None:
        return self._clientes.get(cliente_id)

    def atualizar_saldo(self, cliente_id: int, novo_saldo: float) -> None:
        cliente = self._clientes[cliente_id]
        self._clientes[cliente_id] = Cliente(
            cliente.id, cliente.nome, cliente.email, cliente.senha_hash, novo_saldo, cliente.score
        )

    def atualizar_score(self, cliente_id: int, score: int) -> None:
        cliente = self._clientes[cliente_id]
        self._clientes[cliente_id] = Cliente(
            cliente.id, cliente.nome, cliente.email, cliente.senha_hash, cliente.saldo, score
        )

    def registrar_transacao(self, cliente_id: int, tipo: str, descricao: str, valor: float) -> Transacao:
        transacao = Transacao(
            self._proximo_id_transacao,
            cliente_id,
            tipo,
            descricao,
            valor,
            datetime.now().isoformat(),
        )
        self._proximo_id_transacao += 1
        self._transacoes.append(transacao)
        return transacao

    def listar_transacoes(self, cliente_id: int) -> list[Transacao]:
        return [t for t in self._transacoes if t.cliente_id == cliente_id]