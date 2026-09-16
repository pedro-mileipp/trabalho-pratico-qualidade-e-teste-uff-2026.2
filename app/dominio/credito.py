from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SituacaoCredito(Enum):
    APROVADO = "aprovado"
    NEGADO = "negado"
    PARCIAL = "parcial"


@dataclass
class RegistroHistorico:
    tipo: str
    peso: int = 1


@dataclass
class ResultadoCredito:
    situacao: SituacaoCredito
    score: int
    limite: float
    motivo: str


class DecisorCredito:
    def __init__(
        self,
        score_inicial: int = 500,
        base_limite: float = 1000.0,
        limite_maximo: float = 50000.0,
    ) -> None:
        self._score_inicial = score_inicial
        self._base_limite = base_limite
        self._limite_maximo = limite_maximo

    def calcular_score(self, registros: list[RegistroHistorico]) -> int:
        score = self._score_inicial
        for registro in registros:
            if registro.tipo == "pagamento_em_dia":
                score += registro.peso
            elif registro.tipo == "atraso":
                score -= registro.peso * 2
            elif registro.tipo == "negativacao":
                score -= registro.peso * 5
            elif registro.tipo == "consulta":
                score -= registro.peso
            elif registro.tipo == "cheque_sem_fundos":
                score -= registro.peso * 8
            elif registro.tipo == "contestacao_vencida":
                score -= registro.peso * 3
            elif registro.tipo == "adiantamento":
                score += registro.peso * 2
            else:
                score += 1
            if score < 0:
                score = 0
            if score > 1000:
                score = 1000
        return score

    def limite_por_score(self, score: int, renda: float) -> float:
        if renda <= 0:
            return 0.0
        if score < 300:
            return 0.0
        if score < 500:
            return min(renda * 0.5, self._base_limite * 2)
        if score < 700:
            return min(renda * 1.0, self._base_limite * 10)
        if score < 850:
            return min(renda * 1.5, self._base_limite * 30)
        return min(renda * 2.0, self._limite_maximo)

    def decidir(
        self,
        registros: list[RegistroHistorico],
        renda: float,
        valor_solicitado: float,
    ) -> ResultadoCredito:
        score = self.calcular_score(registros)
        limite = self.limite_por_score(score, renda)
        if score < 300:
            return ResultadoCredito(SituacaoCredito.NEGADO, score, 0, "score_baixo")
        if limite == 0:
            return ResultadoCredito(SituacaoCredito.NEGADO, score, 0, "sem_limite")
        if valor_solicitado <= 0:
            return ResultadoCredito(SituacaoCredito.NEGADO, score, limite, "valor_invalido")
        if valor_solicitado <= limite:
            return ResultadoCredito(SituacaoCredito.APROVADO, score, limite, "aprovado")
        if valor_solicitado <= limite * 1.5:
            return ResultadoCredito(SituacaoCredito.PARCIAL, score, limite, "parcial")
        return ResultadoCredito(SituacaoCredito.NEGADO, score, limite, "acima_limite")