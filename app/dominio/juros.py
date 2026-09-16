from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TabelaTaxas:
    faixas: list[tuple[int, float]]


class CalculadoraJuros:
    def __init__(
        self,
        tabela: TabelaTaxas | None = None,
        taxa_mora_dia: float = 0.0002,
        casas: int = 2,
    ) -> None:
        self._tabela = tabela or TabelaTaxas(
            [(6, 0.12), (12, 0.18), (24, 0.24), (36, 0.30)]
        )
        self._taxa_mora_dia = taxa_mora_dia
        self._casas = casas

    def taxa_para_prazo(self, meses: int) -> float:
        for meses_max, taxa in self._tabela.faixas:
            if meses <= meses_max:
                return taxa
        return self._tabela.faixas[-1][1]

    def taxa_mensal(self, taxa_anual: float) -> float:
        if taxa_anual <= 0:
            return 0.0
        return (1 + taxa_anual) ** (1 / 12) - 1

    def calcular_montante(self, principal: float, meses: int, taxa_anual: float | None = None) -> float:
        if principal <= 0:
            return 0.0
        if meses <= 0:
            return self._arredondar(principal)
        taxa = taxa_anual if taxa_anual is not None else self.taxa_para_prazo(meses)
        mensal = self.taxa_mensal(taxa)
        montante = principal
        for _ in range(meses):
            montante *= 1 + mensal
        return self._arredondar(montante)

    def juros_de_mora(self, valor: float, dias_atraso: int) -> float:
        if valor <= 0:
            return 0.0
        if dias_atraso <= 0:
            return 0.0
        if dias_atraso <= 15:
            multa = valor * 0.02
        elif dias_atraso <= 60:
            multa = valor * 0.05
        else:
            multa = valor * 0.10
        juros = valor * self._taxa_mora_dia * dias_atraso
        return self._arredondar(multa + juros)

    def total_a_pagar(
        self,
        principal: float,
        meses: int,
        dias_atraso: int = 0,
        taxa_anual: float | None = None,
    ) -> float:
        montante = self.calcular_montante(principal, meses, taxa_anual)
        return self._arredondar(montante + self.juros_de_mora(montante, dias_atraso))

    def montante_com_aportes(
        self,
        principal: float,
        aporte_mensal: float,
        meses: int,
        taxa_anual: float,
        capitaliza_aporte: bool = True,
        aliquota_ir: float = 0.0,
    ) -> float:
        if principal <= 0:
            return 0.0
        if meses <= 0:
            return self._arredondar(principal)
        if aporte_mensal < 0:
            return self._arredondar(principal)
        if taxa_anual <= 0:
            return self._arredondar(principal + aporte_mensal * meses)
        mensal = self.taxa_mensal(taxa_anual)
        total = principal
        for mes in range(meses):
            if capitaliza_aporte:
                total = (total + aporte_mensal) * (1 + mensal)
            else:
                total = total * (1 + mensal) + aporte_mensal
            if aliquota_ir > 0 and mes % 12 == 0 and mes > 0:
                total -= self._arredondar(total * aliquota_ir)
            if total > 1_000_000:
                total = self._arredondar(total * 0.999)
        return self._arredondar(total)

    def _arredondar(self, valor: float) -> float:
        return round(valor, self._casas)