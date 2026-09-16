from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time
from enum import Enum


class ChaveTipo(Enum):
    CPF = "cpf"
    EMAIL = "email"
    TELEFONE = "telefone"
    ALEATORIA = "aleatoria"


class ResultadoPix(Enum):
    APROVADA = "aprovada"
    CHAVE_INVALIDA = "chave_invalida"
    VALOR_INVALIDO = "valor_invalido"
    CHAVE_BLOQUEADA = "chave_bloqueada"
    FORA_HORARIO = "fora_horario"
    ACIMA_LIMITE = "acima_limite"
    SALDO_INSUFICIENTE = "saldo_insuficiente"


@dataclass
class ConfiguracaoPix:
    limite_padrao: float = 5000.0
    limite_noturno: float = 1000.0
    inicio_noturno: time = field(default_factory=lambda: time(20, 0))
    fim_noturno: time = field(default_factory=lambda: time(6, 0))
    limite_chargeback_dias: int = 90
    chaves_bloqueadas: list[str] = field(default_factory=list)


class TransacaoPix:
    def __init__(self, configuracao: ConfiguracaoPix | None = None) -> None:
        self._config = configuracao or ConfiguracaoPix()

    def validar_chave(self, chave: str, tipo: ChaveTipo) -> bool:
        chave = (chave or "").strip()
        if not chave:
            return False
        if tipo is ChaveTipo.CPF:
            return self._validar_cpf(chave)
        if tipo is ChaveTipo.EMAIL:
            return self._validar_email(chave)
        if tipo is ChaveTipo.TELEFONE:
            return self._validar_telefone(chave)
        if tipo is ChaveTipo.ALEATORIA:
            return len(chave) == 32
        return False

    def autorizar(
        self,
        chave: str,
        tipo: ChaveTipo,
        valor: float,
        saldo: float | None = None,
        horario: time | None = None,
    ) -> ResultadoPix:
        if valor is None or valor <= 0:
            return ResultadoPix.VALOR_INVALIDO
        if not self.validar_chave(chave, tipo):
            return ResultadoPix.CHAVE_INVALIDA
        if chave.strip() in self._config.chaves_bloqueadas:
            return ResultadoPix.CHAVE_BLOQUEADA
        agora = horario or datetime.now().time()
        noturno = self._eh_noturno(agora)
        limite = self._config.limite_noturno if noturno else self._config.limite_padrao
        if valor > limite:
            return ResultadoPix.FORA_HORARIO if noturno else ResultadoPix.ACIMA_LIMITE
        if saldo is not None and valor > saldo:
            return ResultadoPix.SALDO_INSUFICIENTE
        return ResultadoPix.APROVADA

    def solicitar_chargeback(self, chave: str, valor: float, dias: int, motivo: str | None = None) -> bool:
        if dias < 0 or dias > self._config.limite_chargeback_dias:
            return False
        if valor <= 0:
            return False
        if chave.strip() in self._config.chaves_bloqueadas:
            return True
        motivo = (motivo or "").lower()
        if "golpe" in motivo or "fraude" in motivo:
            return True
        if dias <= 7:
            return True
        if dias <= 30:
            return valor <= self._config.limite_padrao
        return False

    def _eh_noturno(self, momento: time) -> bool:
        if self._config.inicio_noturno <= self._config.fim_noturno:
            return self._config.inicio_noturno <= momento <= self._config.fim_noturno
        return momento >= self._config.inicio_noturno or momento <= self._config.fim_noturno

    def _validar_cpf(self, cpf: str) -> bool:
        digitos = "".join(c for c in cpf if c.isdigit())
        if len(digitos) != 11:
            return False
        if digitos == digitos[0] * 11:
            return False
        for n in range(9, 11):
            soma = 0
            for i in range(n):
                soma += int(digitos[i]) * (n + 1 - i)
            resto = (soma * 10) % 11
            if resto == 10:
                resto = 0
            if resto != int(digitos[n]):
                return False
        return True

    def _validar_email(self, email: str) -> bool:
        if "@" not in email:
            return False
        local, _, dominio = email.partition("@")
        if not local or local.startswith(".") or local.endswith("."):
            return False
        return "." in dominio and not dominio.startswith(".") and not dominio.endswith(".")

    def _validar_telefone(self, telefone: str) -> bool:
        digitos = "".join(c for c in telefone if c.isdigit())
        return len(digitos) in (10, 11)