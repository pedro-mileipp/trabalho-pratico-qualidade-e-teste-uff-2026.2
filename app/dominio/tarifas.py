from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TipoConta(Enum):
    CORRENTE = "corrente"
    POUPANCA = "poupanca"
    PREMIUM = "premium"


@dataclass
class TarifasBase:
    corrente: float = 30.0
    poupanca: float = 0.0
    premium: float = 50.0
    faixas_isencao: tuple[float, float, float] = (1000.0, 5000.0, 50000.0)
    tarifa_por_transacao: float = 2.5
    transacoes_gratuitas: int = 10


class TarifaBancaria:
    def __init__(self, base: TarifasBase | None = None) -> None:
        self._base = base or TarifasBase()

    def tarifa_mensal(
        self,
        tipo: TipoConta,
        saldo: float,
        tem_pacote: bool = False,
        quantidade_transacoes: int = 0,
        antiguidade_meses: int = 0,
    ) -> float:
        if tipo is TipoConta.POUPANCA:
            return 0.0
        if tem_pacote:
            if tipo is TipoConta.PREMIUM and saldo >= self._base.faixas_isencao[2]:
                return 0.0
            if saldo >= self._base.faixas_isencao[1] or antiguidade_meses >= 24:
                base = self._base.corrente * 0.5
            else:
                base = self._base.corrente if tipo is TipoConta.CORRENTE else self._base.premium * 0.7
            return round(base, 2)
        base = self._base.corrente if tipo is TipoConta.CORRENTE else self._base.premium
        if self._tem_isencao(tipo, saldo):
            base = 0.0
        elif antiguidade_meses >= 36:
            base = round(base * 0.8, 2)
        elif saldo < 0:
            base += self._base.corrente * 0.2
        return round(base + self.tarifa_por_transacao_extra(quantidade_transacoes), 2)

    def _tarifa_com_pacote(self, tipo: TipoConta, saldo: float) -> float:
        if tipo is TipoConta.PREMIUM and saldo >= self._base.faixas_isencao[2]:
            return 0.0
        if tipo is TipoConta.CORRENTE:
            return self._base.corrente
        return round(self._base.premium * 0.7, 2)

    def _tem_isencao(self, tipo: TipoConta, saldo: float) -> bool:
        if tipo is TipoConta.PREMIUM:
            return saldo >= self._base.faixas_isencao[2]
        if tipo is TipoConta.CORRENTE:
            return saldo >= self._base.faixas_isencao[1]
        return saldo >= self._base.faixas_isencao[0]

    def tarifa_por_transacao_extra(self, quantidade: int) -> float:
        if quantidade <= self._base.transacoes_gratuitas:
            return 0.0
        return (quantidade - self._base.transacoes_gratuitas) * self._base.tarifa_por_transacao

    def tarifa_anual(
        self,
        tipo: TipoConta,
        saldo: float,
        tem_pacote: bool = False,
        quantidade_transacoes: int = 0,
    ) -> float:
        return round(self.tarifa_mensal(tipo, saldo, tem_pacote, quantidade_transacoes) * 12, 2)