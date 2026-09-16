from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SistemaAmortizacao(Enum):
    PRICE = "price"
    SAC = "sac"


@dataclass
class ResultadoEmprestimo:
    aprovado: bool
    motivo: str
    valor_parcela: float
    numero_parcelas: int
    total_pago: float
    parcelas: list[float]


class SimuladorEmprestimo:
    def __init__(
        self,
        taxa_base: float = 0.03,
        teto_comprometimento: float = 0.30,
        prazo_min: int = 2,
        prazo_max: int = 60,
        valor_minimo: float = 100.0,
    ) -> None:
        self._taxa_base = taxa_base
        self._teto_comprometimento = teto_comprometimento
        self._prazo_min = prazo_min
        self._prazo_max = prazo_max
        self._valor_minimo = valor_minimo

    def taxa_por_prazo(self, meses: int) -> float:
        if meses <= 6:
            return self._taxa_base - 0.005
        if meses <= 12:
            return self._taxa_base
        if meses <= 36:
            return self._taxa_base + 0.005
        return self._taxa_base + 0.01

    def teto_por_renda(self, renda: float) -> float:
        if renda <= 0:
            return 0.0
        if renda < 2000:
            return renda * 0.15
        if renda < 5000:
            return renda * 0.20
        if renda < 10000:
            return renda * 0.25
        return renda * 0.30

    def parcelas_price(self, principal: float, taxa_mensal: float, meses: int) -> list[float]:
        if taxa_mensal == 0:
            return [round(principal / meses, 2)] * meses
        fator = (1 + taxa_mensal) ** meses
        parcela = principal * taxa_mensal * fator / (fator - 1)
        return [round(parcela, 2)] * meses

    def parcelas_sac(self, principal: float, taxa_mensal: float, meses: int) -> list[float]:
        amortizacao = principal / meses
        parcelas: list[float] = []
        saldo = principal
        for _ in range(meses):
            juros = saldo * taxa_mensal
            parcela = amortizacao + juros
            parcelas.append(round(parcela, 2))
            saldo -= amortizacao
        return parcelas

    def simular(
        self,
        principal: float,
        meses: int,
        renda: float,
        sistema: SistemaAmortizacao = SistemaAmortizacao.PRICE,
        score: int | None = None,
        inadimplente: bool = False,
    ) -> ResultadoEmprestimo:
        if principal <= 0:
            return ResultadoEmprestimo(False, "valor_invalido", 0, 0, 0, [])
        if principal < self._valor_minimo:
            return ResultadoEmprestimo(False, "valor_abaixo_minimo", 0, 0, 0, [])
        if meses < self._prazo_min:
            return ResultadoEmprestimo(False, "prazo_curto", 0, 0, 0, [])
        if meses > self._prazo_max:
            return ResultadoEmprestimo(False, "prazo_longo", 0, 0, 0, [])
        if renda <= 0:
            return ResultadoEmprestimo(False, "renda_invalida", 0, 0, 0, [])
        if inadimplente:
            return ResultadoEmprestimo(False, "inadimplente", 0, 0, 0, [])
        if score is not None and score < 400:
            return ResultadoEmprestimo(False, "score_baixo", 0, 0, 0, [])
        teto = self.teto_por_renda(renda)
        if principal > teto:
            return ResultadoEmprestimo(False, "acima_teto", 0, 0, 0, [])
        taxa = self.taxa_por_prazo(meses)
        if sistema is SistemaAmortizacao.SAC:
            parcelas = self.parcelas_sac(principal, taxa, meses)
        else:
            parcelas = self.parcelas_price(principal, taxa, meses)
        primeira = parcelas[0]
        if primeira > renda * self._teto_comprometimento:
            return ResultadoEmprestimo(False, "comprometimento_acima", 0, 0, 0, [])
        total = round(sum(parcelas), 2)
        return ResultadoEmprestimo(True, "aprovado", primeira, meses, total, parcelas)