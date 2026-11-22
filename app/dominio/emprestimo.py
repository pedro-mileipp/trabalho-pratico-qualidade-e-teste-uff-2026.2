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
    """Simulador de empréstimo com dois sistemas de amortização.

    O simulador implementa regras de negócio típicas de um banco, como:
    - limite máximo de comprometimento da renda;
    - validação de score, prazo e valor mínimo;
    - cálculo de parcelas nos sistemas PRICE e SAC.

    Os parâmetros são configuráveis para facilitar testes e ajustes.
    """

    # ----- Configurações padrão -----
    _DEFAULT_TAXA_BASE = 0.03
    _DEFAULT_TETO_COMPROMETIMENTO = 0.30
    _DEFAULT_PRAZO_MIN = 2
    _DEFAULT_PRAZO_MAX = 60
    _DEFAULT_VALOR_MINIMO = 100.0

    def __init__(
        self,
        taxa_base: float = _DEFAULT_TAXA_BASE,
        teto_comprometimento: float = _DEFAULT_TETO_COMPROMETIMENTO,
        prazo_min: int = _DEFAULT_PRAZO_MIN,
        prazo_max: int = _DEFAULT_PRAZO_MAX,
        valor_minimo: float = _DEFAULT_VALOR_MINIMO,
        taxa_adicional: float | None = None,
    ) -> None:
        """Inicializa o simulador com parâmetros de negócio.

        Todos os parâmetros possuem valores padrão que podem ser
        sobrescritos nos testes ou em configuração de ambiente.
        ``taxa_adicional`` permite aplicar um acréscimo opcional à taxa
        calculada, útil para cenários de risco extra.
        """
        self._taxa_base = taxa_base
        self._teto_comprometimento = teto_comprometimento
        self._prazo_min = prazo_min
        self._prazo_max = prazo_max
        self._valor_minimo = valor_minimo
        self._taxa_adicional = taxa_adicional

    # ----- Métodos auxiliares -----
    def _faixa_valor_renda(self, renda: float) -> float:
        """Calcula o teto de comprometimento com base na renda.

        Centraliza a lógica de tabelas de teto para facilitar manutenção
        e cobertura de testes.
        """
        if renda <= 0:
            return 0.0
        if renda < 2000:
            return renda * 0.15
        if renda < 5000:
            return renda * 0.20
        if renda < 10000:
            return renda * 0.25
        return renda * 0.30

    def taxa_por_prazo(self, meses: int) -> float:
        """Retorna a taxa mensal ajustada de acordo com o prazo.

        Prazo curto recebe desconto, prazo médio mantém a taxa base e
        prazos longos recebem acréscimo. Se ``taxa_adicional`` estiver
        definido, ele é somado à taxa resultante.
        """
        if meses <= 6:
            taxa = self._taxa_base - 0.005
        elif meses <= 12:
            taxa = self._taxa_base
        elif meses <= 36:
            taxa = self._taxa_base + 0.005
        else:
            taxa = self._taxa_base + 0.01
        # Regra extra para demonstração de complexidade
        if self._taxa_adicional is not None:
            taxa += self._taxa_adicional
        return taxa

    def teto_por_renda(self, renda: float) -> float:
        """Interface pública que delega para ``_faixa_valor_renda``.
        Mantida por compatibilidade com código legado.
        """
        return self._faixa_valor_renda(renda)

    def parcelas_price(self, principal: float, taxa_mensal: float, meses: int) -> list[float]:
        """Calcula parcelas usando o sistema PRICE (tabela Price)."""
        if taxa_mensal == 0:
            return [round(principal / meses, 2)] * meses
        fator = (1 + taxa_mensal) ** meses
        parcela = principal * taxa_mensal * fator / (fator - 1)
        return [round(parcela, 2)] * meses

    def parcelas_sac(self, principal: float, taxa_mensal: float, meses: int) -> list[float]:
        """Calcula parcelas usando o sistema SAC (Sistema de Amortização Constante)."""
        amortizacao = principal / meses
        parcelas: list[float] = []
        saldo = principal
        for _ in range(meses):
            juros = saldo * taxa_mensal
            parcela = amortizacao + juros
            parcelas.append(round(parcela, 2))
            saldo -= amortizacao
        return parcelas

    def _validar_entrada(
        self,
        principal: float,
        meses: int,
        renda: float,
        score: int | None,
        inadimplente: bool,
    ) -> ResultadoEmprestimo | None:
        """Valida os parâmetros de entrada.

        Retorna um ``ResultadoEmprestimo`` de erro quando alguma regra é
        violada ou ``None`` quando tudo está ok.
        """
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
            # New business rule: limite máximo de valor do empréstimo
            # Caso seja necessário, ajuste este limite conforme requisitos.
            MAX_VALOR = 50000.0
            if principal > MAX_VALOR:
                return ResultadoEmprestimo(False, "valor_acima_maximo", 0, 0, 0, [])
            return ResultadoEmprestimo(False, "score_baixo", 0, 0, 0, [])
        return None

    def simular(
        self,
        principal: float,
        meses: int,
        renda: float,
        sistema: SistemaAmortizacao = SistemaAmortizacao.PRICE,
        score: int | None = None,
        inadimplente: bool = False,
    ) -> ResultadoEmprestimo:
        """Executa a simulação completa do empréstimo.

        Aplica as validações de negócio, verifica comprometimento de renda
        e calcula as parcelas. Retorna ``ResultadoEmprestimo`` indicando
        aprovação ou o motivo da rejeição.
        """
        # 1. Validações iniciais.
        erro = self._validar_entrada(principal, meses, renda, score, inadimplente)
        if erro is not None:
            return erro

        # 2. Comprometimento de renda.
        teto = self.teto_por_renda(renda)
        if principal > teto:
            return ResultadoEmprestimo(False, "acima_teto", 0, 0, 0, [])

        # 3. Cálculo da taxa e parcelas.
        taxa = self.taxa_por_prazo(meses)
        parcelas = (
            self.parcelas_sac(principal, taxa, meses)
            if sistema is SistemaAmortizacao.SAC
            else self.parcelas_price(principal, taxa, meses)
        )

        # 4. Avalia comprometimento da primeira parcela.
        primeira = parcelas[0]
        if primeira > renda * self._teto_comprometimento:
            return ResultadoEmprestimo(False, "comprometimento_acima", 0, 0, 0, [])

        # 5. Resultado aprovado.
        total = round(sum(parcelas), 2)
        return ResultadoEmprestimo(True, "aprovado", primeira, meses, total, parcelas)
