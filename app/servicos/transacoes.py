from __future__ import annotations

from datetime import datetime

from app.dominio.pix import ChaveTipo, ConfiguracaoPix, ResultadoPix, TransacaoPix
from app.repositorios.repositorio import Repositorio


class TransacaoRecusada(Exception):
    def __init__(self, resultado: ResultadoPix) -> None:
        self.resultado = resultado
        super().__init__(resultado.value)


class TransacaoService:
    def __init__(
        self,
        repositorio: Repositorio,
        config_pix: ConfiguracaoPix | None = None,
    ) -> None:
        self._repositorio = repositorio
        self._pix = TransacaoPix(config_pix)

    def transferir_pix(
        self,
        cliente_id: int,
        chave: str,
        tipo: ChaveTipo,
        valor: float,
        horario: datetime | None = None,
    ) -> float:
        cliente = self._repositorio.buscar_cliente_por_id(cliente_id)
        if cliente is None:
            raise TransacaoRecusada(ResultadoPix.CHAVE_INVALIDA)
        resultado = self._pix.autorizar(chave, tipo, valor, cliente.saldo, horario)
        if resultado is not ResultadoPix.APROVADA:
            raise TransacaoRecusada(resultado)
        novo_saldo = cliente.saldo - valor
        self._repositorio.atualizar_saldo(cliente_id, novo_saldo)
        self._repositorio.registrar_transacao(cliente_id, "pix", f"PIX {tipo.value}", -valor)
        return novo_saldo