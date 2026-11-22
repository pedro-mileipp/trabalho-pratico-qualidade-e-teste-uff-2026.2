"""Testes unitários de SimuladorEmprestimo (app/dominio/emprestimo.py).

Técnica de cada caso, indicada pelo prefixo do id do ``pytest.param`` ou pelo nome do teste:
    pe_     partição de equivalência
    vl_     análise de valor-limite
    td_     tabela de decisão
    laco_   teste de laços
    custom_ parâmetros do construtor (taxa_base, teto_comprometimento, prazo_min, prazo_max, valor_minimo)

Cobertura estrutural (todas-arestas) e resultados: docs/relatorios/cobertura_mutacao.md.

Decisão de projeto: simular() avalia as regras na ordem:
    principal <= 0 ("valor_invalido")
    -> principal < valor_minimo ("valor_abaixo_minimo")
    -> meses < prazo_min ("prazo_curto")
    -> meses > prazo_max ("prazo_longo")
    -> renda <= 0 ("renda_invalida")
    -> inadimplente ("inadimplente")
    -> score < 400 ("score_baixo")
    -> principal > teto_por_renda ("acima_teto")
    -> primeira_parcela > renda * teto_comprometimento ("comprometimento_acima")
    -> aprovado (Price ou SAC)
"""

from __future__ import annotations

import pytest

from app.dominio.emprestimo import (
    SimuladorEmprestimo,
    SistemaAmortizacao,
)


@pytest.fixture
def simulador() -> SimuladorEmprestimo:
    """Simulador com configurações padrão."""
    return SimuladorEmprestimo()


@pytest.fixture
def simulador_custom() -> SimuladorEmprestimo:
    """Simulador com parâmetros customizados."""
    return SimuladorEmprestimo(
        taxa_base=0.05,
        teto_comprometimento=0.20,
        prazo_min=6,
        prazo_max=36,
        valor_minimo=500.0,
    )


# ==============================================================================
# 1. taxa_por_prazo: Partição de Equivalência (PE) e Análise de Valor-Limite (AVL)
# ==============================================================================


class TestTaxaPorPrazo:
    """Testes de taxa_por_prazo aplicando Partição de Equivalência e Análise de Valor-Limite."""

    @pytest.mark.parametrize(
        ("meses", "taxa_esperada"),
        [
            # Partição de Equivalência (classes válidas de prazo)
            pytest.param(3, 0.025, id="pe_faixa1_ate_6_meses"),
            pytest.param(9, 0.030, id="pe_faixa2_7_a_12_meses"),
            pytest.param(24, 0.035, id="pe_faixa3_13_a_36_meses"),
            pytest.param(48, 0.040, id="pe_faixa4_acima_36_meses"),
            # Análise de Valor-Limite (fronteiras com passo unitário)
            pytest.param(0, 0.025, id="vl_meses_zero_abaixo_piso"),
            pytest.param(1, 0.025, id="vl_meses_um_logo_abaixo_prazo_min"),
            pytest.param(2, 0.025, id="vl_faixa1_piso_prazo_min"),
            pytest.param(5, 0.025, id="vl_faixa1_logo_abaixo_fronteira"),
            pytest.param(6, 0.025, id="vl_faixa1_teto_fronteira_6"),
            pytest.param(7, 0.030, id="vl_faixa2_piso_fronteira_7"),
            pytest.param(11, 0.030, id="vl_faixa2_logo_abaixo_fronteira"),
            pytest.param(12, 0.030, id="vl_faixa2_teto_fronteira_12"),
            pytest.param(13, 0.035, id="vl_faixa3_piso_fronteira_13"),
            pytest.param(35, 0.035, id="vl_faixa3_logo_abaixo_fronteira"),
            pytest.param(36, 0.035, id="vl_faixa3_teto_fronteira_36"),
            pytest.param(37, 0.040, id="vl_faixa4_piso_fronteira_37"),
            pytest.param(60, 0.040, id="vl_faixa4_teto_prazo_max"),
        ],
    )
    def test_taxa_por_prazo(self, simulador: SimuladorEmprestimo, meses: int, taxa_esperada: float):
        assert simulador.taxa_por_prazo(meses) == pytest.approx(taxa_esperada)


# ==============================================================================
# 2. teto_por_renda: Partição de Equivalência (PE) e Análise de Valor-Limite (AVL)
# ==============================================================================


class TestTetoPorRenda:
    """Testes de teto_por_renda aplicando Partição de Equivalência e Análise de Valor-Limite."""

    @pytest.mark.parametrize(
        ("renda", "teto_esperado"),
        [
            # Partição de Equivalência (classes típicas)
            pytest.param(-100.0, 0.0, id="pe_renda_negativa_invalida"),
            pytest.param(1000.0, 150.0, id="pe_faixa1_renda_baixa_15_pct"),
            pytest.param(3000.0, 600.0, id="pe_faixa2_renda_media_baixa_20_pct"),
            pytest.param(7000.0, 1750.0, id="pe_faixa3_renda_media_alta_25_pct"),
            pytest.param(15000.0, 4500.0, id="pe_faixa4_renda_alta_30_pct"),
            # Análise de Valor-Limite (fronteiras com passo centesimal)
            pytest.param(-0.01, 0.0, id="vl_renda_logo_abaixo_zero"),
            pytest.param(0.0, 0.0, id="vl_renda_zero_exato"),
            pytest.param(0.01, 0.0015, id="vl_faixa1_piso_logo_acima_zero"),
            pytest.param(1999.99, 299.9985, id="vl_faixa1_teto_fronteira_2000"),
            pytest.param(2000.0, 400.0, id="vl_faixa2_piso_fronteira_2000"),
            pytest.param(2000.01, 400.002, id="vl_faixa2_logo_acima_fronteira_2000"),
            pytest.param(4999.99, 999.998, id="vl_faixa2_teto_fronteira_5000"),
            pytest.param(5000.0, 1250.0, id="vl_faixa3_piso_fronteira_5000"),
            pytest.param(5000.01, 1250.0025, id="vl_faixa3_logo_acima_fronteira_5000"),
            pytest.param(9999.99, 2499.9975, id="vl_faixa3_teto_fronteira_10000"),
            pytest.param(10000.0, 3000.0, id="vl_faixa4_piso_fronteira_10000"),
            pytest.param(10000.01, 3000.003, id="vl_faixa4_logo_acima_fronteira_10000"),
        ],
    )
    def test_teto_por_renda(self, simulador: SimuladorEmprestimo, renda: float, teto_esperado: float):
        assert simulador.teto_por_renda(renda) == pytest.approx(teto_esperado)


# ==============================================================================
# 3. Parcelas Price e SAC: Testes de Laços (Loop Testing) e Cálculos Numéricos
# ==============================================================================


class TestParcelas:
    """Testes detalhados de amortização Price e SAC com foco em Teste de Laços e precisão numérica."""

    # --- Amortização Price ---

    def test_parcelas_price_taxa_zero(self, simulador: SimuladorEmprestimo):
        """Partição com taxa zero: parcelas puramente lineares."""
        parcelas = simulador.parcelas_price(1000.0, 0.0, 10)
        assert len(parcelas) == 10
        assert parcelas == [100.0] * 10
        assert round(sum(parcelas), 2) == 1000.0

    def test_parcelas_price_taxa_zero_um_mes(self, simulador: SimuladorEmprestimo):
        """Fronteira de 1 mês com taxa zero."""
        parcelas = simulador.parcelas_price(500.0, 0.0, 1)
        assert parcelas == [500.0]

    @pytest.mark.parametrize(
        ("principal", "taxa", "meses", "parcela_esperada", "total_esperado"),
        [
            pytest.param(1000.0, 0.025, 2, 518.83, 1037.66, id="pe_price_2_meses_taxa_025"),
            pytest.param(1000.0, 0.030, 5, 218.35, 1091.75, id="pe_price_5_meses_taxa_030"),
            pytest.param(1000.0, 0.025, 6, 181.55, 1089.30, id="pe_price_6_meses_taxa_025"),
            pytest.param(1200.0, 0.030, 12, 120.55, 1446.60, id="pe_price_12_meses_taxa_030"),
            pytest.param(2400.0, 0.035, 24, 149.45, 3586.80, id="pe_price_24_meses_taxa_035"),
            pytest.param(3000.0, 0.040, 60, 132.61, 7956.60, id="pe_price_60_meses_taxa_040"),
        ],
    )
    def test_parcelas_price_valores_exatos(
        self,
        simulador: SimuladorEmprestimo,
        principal: float,
        taxa: float,
        meses: int,
        parcela_esperada: float,
        total_esperado: float,
    ):
        """Validação numérica exata de cada parcela Price e do montante acumulado."""
        parcelas = simulador.parcelas_price(principal, taxa, meses)
        assert len(parcelas) == meses
        assert parcelas == [parcela_esperada] * meses
        assert round(sum(parcelas), 2) == total_esperado

    # --- Amortização SAC (Teste de Laços: 0, 1, 2, n, max-1, max, max+1) ---

    def test_parcelas_sac_taxa_zero(self, simulador: SimuladorEmprestimo):
        """SAC com taxa zero: parcelas iguais à amortização pura."""
        parcelas = simulador.parcelas_sac(1000.0, 0.0, 4)
        assert len(parcelas) == 4
        assert parcelas == [250.0, 250.0, 250.0, 250.0]
        assert round(sum(parcelas), 2) == 1000.0

    def test_parcelas_sac_laco_zero_iteracoes(self, simulador: SimuladorEmprestimo):
        """Teste de laço: 0 iterações (meses = 0). Lança ZeroDivisionError na amortização."""
        with pytest.raises(ZeroDivisionError):
            simulador.parcelas_sac(1000.0, 0.03, 0)

    def test_parcelas_sac_laco_uma_iteracao(self, simulador: SimuladorEmprestimo):
        """Teste de laço: 1 iteração (meses = 1). Amortização = principal, juros = principal * taxa."""
        parcelas = simulador.parcelas_sac(1000.0, 0.03, 1)
        assert len(parcelas) == 1
        assert parcelas == [1030.0]
        assert round(sum(parcelas), 2) == 1030.0

    def test_parcelas_sac_laco_duas_iteracoes_piso(self, simulador: SimuladorEmprestimo):
        """Teste de laço: 2 iterações (meses = 2, piso aceito pelo sistema)."""
        parcelas = simulador.parcelas_sac(1000.0, 0.025, 2)
        assert len(parcelas) == 2
        # Amortização: 500.0
        # Mês 1: Saldo 1000.0 -> Juros 25.0 -> Parcela 525.0 -> Saldo 500.0
        # Mês 2: Saldo 500.0  -> Juros 12.5 -> Parcela 512.5 -> Saldo 0.0
        assert parcelas == [525.0, 512.5]
        assert round(sum(parcelas), 2) == 1037.5

    def test_parcelas_sac_laco_n_iteracoes_tipico(self, simulador: SimuladorEmprestimo):
        """Teste de laço: n iterações (meses = 4), verificando decréscimo estrito dos juros."""
        parcelas = simulador.parcelas_sac(1000.0, 0.03, 4)
        assert len(parcelas) == 4
        assert parcelas == [280.0, 272.5, 265.0, 257.5]
        assert round(sum(parcelas), 2) == 1075.0

    def test_parcelas_sac_laco_n_iteracoes_12_meses(self, simulador: SimuladorEmprestimo):
        """Teste de laço: 12 iterações com valores exatos conferidos."""
        parcelas = simulador.parcelas_sac(1200.0, 0.03, 12)
        assert len(parcelas) == 12
        # Amortização = 100.0 por mês
        esperadas = [136.0, 133.0, 130.0, 127.0, 124.0, 121.0, 118.0, 115.0, 112.0, 109.0, 106.0, 103.0]
        assert parcelas == esperadas
        assert round(sum(parcelas), 2) == 1434.0

    def test_parcelas_sac_laco_max_menos_um_iteracoes(self, simulador: SimuladorEmprestimo):
        """Teste de laço: max - 1 iterações (meses = 59)."""
        parcelas = simulador.parcelas_sac(5900.0, 0.04, 59)
        assert len(parcelas) == 59
        # Amortização = 100.0
        assert parcelas[0] == 336.0  # 100 + 5900 * 0.04 = 100 + 236 = 336.0
        assert parcelas[-1] == 104.0  # 100 + 100 * 0.04 = 100 + 4 = 104.0
        assert round(sum(parcelas), 2) == round(5900.0 + 59 * 60 / 2 * 100.0 * 0.04, 2)

    def test_parcelas_sac_laco_max_iteracoes(self, simulador: SimuladorEmprestimo):
        """Teste de laço: max iterações (meses = 60, teto máximo do sistema)."""
        parcelas = simulador.parcelas_sac(3000.0, 0.04, 60)
        assert len(parcelas) == 60
        # Amortização = 50.0 por mês
        assert parcelas[0] == 170.0  # 50 + 3000 * 0.04 = 170.0
        assert parcelas[-1] == 52.0  # 50 + 50 * 0.04 = 52.0
        assert round(sum(parcelas), 2) == 6660.0

    def test_parcelas_sac_laco_max_mais_um_iteracoes(self, simulador: SimuladorEmprestimo):
        """Teste de laço: max + 1 iterações (meses = 61 direto no método de amortização)."""
        parcelas = simulador.parcelas_sac(6100.0, 0.04, 61)
        assert len(parcelas) == 61
        assert parcelas[0] == 344.0  # 100 + 6100 * 0.04 = 344.0
        assert parcelas[-1] == 104.0  # 100 + 100 * 0.04 = 104.0


# ==============================================================================
# 4. simular: Validações Iniciais (PE e AVL)
# ==============================================================================


class TestSimularValidacoes:
    """Testes de validações e condições de contorno de simular() com PE e AVL."""

    @pytest.mark.parametrize(
        ("principal", "meses", "renda", "inadimplente", "score", "esperado_motivo"),
        [
            # --- Partição de Equivalência (erros típicos) ---
            pytest.param(-500.0, 12, 5000.0, False, 500, "valor_invalido", id="pe_principal_negativo"),
            pytest.param(0.0, 12, 5000.0, False, 500, "valor_invalido", id="pe_principal_zero"),
            pytest.param(50.0, 12, 5000.0, False, 500, "valor_abaixo_minimo", id="pe_principal_abaixo_minimo"),
            pytest.param(1000.0, 1, 5000.0, False, 500, "prazo_curto", id="pe_prazo_abaixo_minimo"),
            pytest.param(1000.0, 72, 5000.0, False, 500, "prazo_longo", id="pe_prazo_acima_maximo"),
            pytest.param(1000.0, 12, 0.0, False, 500, "renda_invalida", id="pe_renda_zero"),
            pytest.param(1000.0, 12, -2000.0, False, 500, "renda_invalida", id="pe_renda_negativa"),
            pytest.param(1000.0, 12, 5000.0, True, 500, "inadimplente", id="pe_cliente_inadimplente"),
            pytest.param(1000.0, 12, 5000.0, False, 250, "score_baixo", id="pe_score_insuficiente"),
            # --- Análise de Valor-Limite (fronteiras de erro) ---
            pytest.param(-0.01, 12, 5000.0, False, 500, "valor_invalido", id="vl_principal_logo_abaixo_zero"),
            pytest.param(0.01, 12, 5000.0, False, 500, "valor_abaixo_minimo", id="vl_principal_logo_acima_zero"),
            pytest.param(99.99, 12, 5000.0, False, 500, "valor_abaixo_minimo", id="vl_principal_logo_abaixo_minimo"),
            pytest.param(1000.0, 0, 5000.0, False, 500, "prazo_curto", id="vl_prazo_zero"),
            pytest.param(1000.0, 61, 5000.0, False, 500, "prazo_longo", id="vl_prazo_logo_acima_maximo"),
            pytest.param(1000.0, 12, -0.01, False, 500, "renda_invalida", id="vl_renda_logo_abaixo_zero"),
            pytest.param(1000.0, 12, 5000.0, False, 398, "score_baixo", id="vl_score_398_baixo"),
            pytest.param(1000.0, 12, 5000.0, False, 399, "score_baixo", id="vl_score_399_fronteira_rejeicao"),
        ],
    )
    def test_simular_validacoes_entradas(
        self,
        simulador: SimuladorEmprestimo,
        principal: float,
        meses: int,
        renda: float,
        inadimplente: bool,
        score: int | None,
        esperado_motivo: str,
    ):
        resultado = simulador.simular(
            principal=principal,
            meses=meses,
            renda=renda,
            inadimplente=inadimplente,
            score=score,
        )
        assert resultado.aprovado is False
        assert resultado.motivo == esperado_motivo
        assert resultado.valor_parcela == 0.0
        assert resultado.numero_parcelas == 0
        assert resultado.total_pago == 0.0
        assert resultado.parcelas == []


# ==============================================================================
# 5. simular: Tabela de Decisão (TD) e Ordem de Precedência das Regras
# ==============================================================================


class TestSimularTabelaDecisao:
    """Tabela de decisão de simular() e precedência entre regras em conflito.

    Ordem de avaliação das regras no código:
        R1: principal <= 0                      -> valor_invalido
        R2: principal < valor_minimo            -> valor_abaixo_minimo
        R3: meses < prazo_min                   -> prazo_curto
        R4: meses > prazo_max                   -> prazo_longo
        R5: renda <= 0                          -> renda_invalida
        R6: inadimplente                        -> inadimplente
        R7: score is not None and score < 400   -> score_baixo
        R8: principal > teto_por_renda          -> acima_teto
        R9: primeira > renda * teto_comp        -> comprometimento_acima
        R10: sistema PRICE                      -> aprovado
        R11: sistema SAC                        -> aprovado
    """

    @pytest.mark.parametrize(
        ("principal", "meses", "renda", "sistema", "score", "inadimplente", "aprovado", "motivo"),
        [
            # --- Regras Base R1 a R11 (caminhos canônicos) ---
            pytest.param(0.0, 12, 5000.0, SistemaAmortizacao.PRICE, 500, False, False, "valor_invalido", id="td_r1_valor_invalido"),
            pytest.param(90.0, 12, 5000.0, SistemaAmortizacao.PRICE, 500, False, False, "valor_abaixo_minimo", id="td_r2_valor_abaixo_minimo"),
            pytest.param(500.0, 1, 5000.0, SistemaAmortizacao.PRICE, 500, False, False, "prazo_curto", id="td_r3_prazo_curto"),
            pytest.param(500.0, 65, 5000.0, SistemaAmortizacao.PRICE, 500, False, False, "prazo_longo", id="td_r4_prazo_longo"),
            pytest.param(500.0, 12, 0.0, SistemaAmortizacao.PRICE, 500, False, False, "renda_invalida", id="td_r5_renda_invalida"),
            pytest.param(500.0, 12, 5000.0, SistemaAmortizacao.PRICE, 500, True, False, "inadimplente", id="td_r6_inadimplente"),
            pytest.param(500.0, 12, 5000.0, SistemaAmortizacao.PRICE, 350, False, False, "score_baixo", id="td_r7_score_baixo"),
            pytest.param(2000.0, 12, 5000.0, SistemaAmortizacao.PRICE, 500, False, False, "acima_teto", id="td_r8_acima_teto"),
            pytest.param(1000.0, 10, 10000.0, SistemaAmortizacao.PRICE, 500, False, True, "aprovado", id="td_r10_aprovado_price"),
            pytest.param(1000.0, 4, 10000.0, SistemaAmortizacao.SAC, 500, False, True, "aprovado", id="td_r11_aprovado_sac"),
            # --- Precedência de Regras (mais de uma condição violada simultaneamente) ---
            pytest.param(0.0, 12, -100.0, SistemaAmortizacao.PRICE, 500, False, False, "valor_invalido", id="td_r1_precedencia_sobre_renda_negativa"),
            pytest.param(-50.0, 12, 5000.0, SistemaAmortizacao.PRICE, 500, True, False, "valor_invalido", id="td_r1_precedencia_sobre_inadimplente"),
            pytest.param(50.0, 1, 5000.0, SistemaAmortizacao.PRICE, 500, False, False, "valor_abaixo_minimo", id="td_r2_precedencia_sobre_prazo_curto"),
            pytest.param(80.0, 12, 5000.0, SistemaAmortizacao.PRICE, 200, False, False, "valor_abaixo_minimo", id="td_r2_precedencia_sobre_score_baixo"),
            pytest.param(500.0, 1, 0.0, SistemaAmortizacao.PRICE, 500, False, False, "prazo_curto", id="td_r3_precedencia_sobre_renda_zero"),
            pytest.param(500.0, 1, 5000.0, SistemaAmortizacao.PRICE, 500, True, False, "prazo_curto", id="td_r3_precedencia_sobre_inadimplente"),
            pytest.param(500.0, 70, 5000.0, SistemaAmortizacao.PRICE, 500, True, False, "prazo_longo", id="td_r4_precedencia_sobre_inadimplente"),
            pytest.param(500.0, 65, 5000.0, SistemaAmortizacao.PRICE, 300, False, False, "prazo_longo", id="td_r4_precedencia_sobre_score_baixo"),
            pytest.param(500.0, 12, -10.0, SistemaAmortizacao.PRICE, 500, True, False, "renda_invalida", id="td_r5_precedencia_sobre_inadimplente"),
            pytest.param(500.0, 12, 0.0, SistemaAmortizacao.PRICE, 150, False, False, "renda_invalida", id="td_r5_precedencia_sobre_score_baixo"),
            pytest.param(500.0, 12, 5000.0, SistemaAmortizacao.PRICE, 250, True, False, "inadimplente", id="td_r6_precedencia_sobre_score_baixo"),
            pytest.param(50000.0, 12, 5000.0, SistemaAmortizacao.PRICE, 500, True, False, "inadimplente", id="td_r6_precedencia_sobre_acima_teto"),
            pytest.param(50000.0, 12, 5000.0, SistemaAmortizacao.PRICE, 350, False, False, "score_baixo", id="td_r7_precedencia_sobre_acima_teto"),
        ],
    )
    def test_simular_tabela_de_decisao(
        self,
        simulador: SimuladorEmprestimo,
        principal: float,
        meses: int,
        renda: float,
        sistema: SistemaAmortizacao,
        score: int | None,
        inadimplente: bool,
        aprovado: bool,
        motivo: str,
    ):
        resultado = simulador.simular(
            principal=principal,
            meses=meses,
            renda=renda,
            sistema=sistema,
            score=score,
            inadimplente=inadimplente,
        )
        assert resultado.aprovado is aprovado
        assert resultado.motivo == motivo

    def test_td_r8_precedencia_acima_teto_sobre_comprometimento_acima(self):
        """R8 (acima_teto) deve prevalecer sobre R9 (comprometimento_acima)."""
        simulador_estrito = SimuladorEmprestimo(teto_comprometimento=0.01)
        # Renda 10000 -> Teto = 3000. Principal = 3500 (> 3000).
        # A parcela também ultrapassaria 1% de 10000 (100), mas acima_teto deve disparar primeiro.
        resultado = simulador_estrito.simular(principal=3500.0, meses=12, renda=10000.0)
        assert resultado.aprovado is False
        assert resultado.motivo == "acima_teto"


# ==============================================================================
# 6. simular: Fronteiras de Teto por Renda e Comprometimento (AVL)
# ==============================================================================


class TestSimularFronteirasNegocio:
    """Análise de valor-limite sobre as decisões de negócio (teto de renda e comprometimento)."""

    @pytest.mark.parametrize(
        ("renda", "principal", "esperado_aprovado", "esperado_motivo"),
        [
            # Faixa 1: Renda < 2000 (15%). Renda 1000 -> Teto = 150.00
            pytest.param(1000.0, 150.00, True, "aprovado", id="vl_teto_faixa1_igual_teto"),
            pytest.param(1000.0, 150.01, False, "acima_teto", id="vl_teto_faixa1_logo_acima_teto"),
            # Faixa 2: Renda 2000 a 4999 (20%). Renda 2000 -> Teto = 400.00
            pytest.param(2000.0, 400.00, True, "aprovado", id="vl_teto_faixa2_igual_teto"),
            pytest.param(2000.0, 400.01, False, "acima_teto", id="vl_teto_faixa2_logo_acima_teto"),
            # Faixa 3: Renda 5000 a 9999 (25%). Renda 5000 -> Teto = 1250.00
            pytest.param(5000.0, 1250.00, True, "aprovado", id="vl_teto_faixa3_igual_teto"),
            pytest.param(5000.0, 1250.01, False, "acima_teto", id="vl_teto_faixa3_logo_acima_teto"),
            # Faixa 4: Renda >= 10000 (30%). Renda 10000 -> Teto = 3000.00
            pytest.param(10000.0, 3000.00, True, "aprovado", id="vl_teto_faixa4_igual_teto"),
            pytest.param(10000.0, 3000.01, False, "acima_teto", id="vl_teto_faixa4_logo_acima_teto"),
        ],
    )
    def test_fronteiras_teto_por_renda(
        self,
        simulador: SimuladorEmprestimo,
        renda: float,
        principal: float,
        esperado_aprovado: bool,
        esperado_motivo: str,
    ):
        resultado = simulador.simular(principal=principal, meses=12, renda=renda)
        assert resultado.aprovado is esperado_aprovado
        assert resultado.motivo == esperado_motivo

    def test_fronteira_comprometimento_price(self):
        """AVL na fronteira de comprometimento de renda para o sistema Price."""
        # Simulador com teto_comprometimento = 10% da renda
        sim = SimuladorEmprestimo(teto_comprometimento=0.10)
        # Renda 2000 -> Teto = 400 (20%). Limite da parcela = 2000 * 0.10 = 200.00
        # Em 2 meses (taxa 0.025):
        # Principal 385 -> parcela = 199.75 <= 200.00 (Aprovado)
        res_ok = sim.simular(principal=385.0, meses=2, renda=2000.0, sistema=SistemaAmortizacao.PRICE)
        assert res_ok.aprovado is True
        assert res_ok.motivo == "aprovado"
        assert res_ok.valor_parcela == 199.75

        # Principal 386 -> parcela = 200.27 > 200.00 (Recusado por comprometimento)
        res_nok = sim.simular(principal=386.0, meses=2, renda=2000.0, sistema=SistemaAmortizacao.PRICE)
        assert res_nok.aprovado is False
        assert res_nok.motivo == "comprometimento_acima"

    def test_fronteira_comprometimento_sac(self):
        """AVL na fronteira de comprometimento de renda para o sistema SAC."""
        sim = SimuladorEmprestimo(teto_comprometimento=0.10)
        # Renda 2000 -> Teto = 400. Limite da primeira parcela = 200.00
        # Em 2 meses (taxa 0.025):
        # Principal 380 -> primeira parcela = 190 + 380 * 0.025 = 199.50 <= 200.00 (Aprovado)
        res_ok = sim.simular(principal=380.0, meses=2, renda=2000.0, sistema=SistemaAmortizacao.SAC)
        assert res_ok.aprovado is True
        assert res_ok.motivo == "aprovado"
        assert res_ok.valor_parcela == 199.50

        # Principal 381 -> primeira parcela = 190.5 + 381 * 0.025 = 200.03 > 200.00 (Recusado)
        res_nok = sim.simular(principal=381.0, meses=2, renda=2000.0, sistema=SistemaAmortizacao.SAC)
        assert res_nok.aprovado is False
        assert res_nok.motivo == "comprometimento_acima"

    @pytest.mark.parametrize(
        ("score", "esperado_motivo"),
        [
            pytest.param(399, "score_baixo", id="vl_score_399_recusado"),
            pytest.param(400, "aprovado", id="vl_score_400_aprovado_piso_exato"),
            pytest.param(401, "aprovado", id="vl_score_401_aprovado"),
            pytest.param(None, "aprovado", id="vl_score_none_sem_restricao"),
            pytest.param(1000, "aprovado", id="vl_score_1000_teto_maximo"),
        ],
    )
    def test_fronteira_score_aprovacao(self, simulador: SimuladorEmprestimo, score: int | None, esperado_motivo: str):
        resultado = simulador.simular(principal=1000.0, meses=12, renda=10000.0, score=score)
        assert resultado.motivo == esperado_motivo
        assert resultado.aprovado is (esperado_motivo == "aprovado")

    @pytest.mark.parametrize(
        ("principal", "meses", "esperado_motivo"),
        [
            pytest.param(100.0, 12, "aprovado", id="vl_principal_100_piso_exato"),
            pytest.param(1000.0, 2, "aprovado", id="vl_prazo_2_piso_exato"),
            pytest.param(1000.0, 60, "aprovado", id="vl_prazo_60_teto_exato"),
        ],
    )
    def test_fronteira_valores_e_prazos_piso_teto_aprovados(
        self,
        simulador: SimuladorEmprestimo,
        principal: float,
        meses: int,
        esperado_motivo: str,
    ):
        resultado = simulador.simular(principal=principal, meses=meses, renda=10000.0)
        assert resultado.aprovado is True
        assert resultado.motivo == esperado_motivo


# ==============================================================================
# 7. simular: Conferência Completa de Resultados Aprovados (Price e SAC)
# ==============================================================================


class TestSimularResultadosCompletos:
    """Verificação rigorosa de todos os campos do ResultadoEmprestimo (mata mutantes numéricos)."""

    def test_simular_aprovado_price_conferencia_campos(self, simulador: SimuladorEmprestimo):
        """Conferência estrita de todos os atributos para empréstimo Price aprovado."""
        resultado = simulador.simular(
            principal=1000.0,
            meses=10,
            renda=10000.0,
            sistema=SistemaAmortizacao.PRICE,
        )
        assert resultado.aprovado is True
        assert resultado.motivo == "aprovado"
        assert resultado.numero_parcelas == 10
        assert resultado.valor_parcela == 117.23
        assert len(resultado.parcelas) == 10
        assert resultado.parcelas == [117.23] * 10
        assert resultado.total_pago == 1172.30

    def test_simular_aprovado_sac_conferencia_campos(self, simulador: SimuladorEmprestimo):
        """Conferência estrita de todos os atributos para empréstimo SAC aprovado."""
        resultado = simulador.simular(
            principal=1000.0,
            meses=4,
            renda=10000.0,
            sistema=SistemaAmortizacao.SAC,
        )
        assert resultado.aprovado is True
        assert resultado.motivo == "aprovado"
        assert resultado.numero_parcelas == 4
        assert resultado.valor_parcela == 275.0
        assert len(resultado.parcelas) == 4
        assert resultado.parcelas == [275.0, 268.75, 262.5, 256.25]
        assert resultado.total_pago == 1062.50

    def test_simular_aprovado_price_2_meses_faixa_minima(self, simulador: SimuladorEmprestimo):
        """Price no prazo mínimo de 2 meses com conferência exata."""
        resultado = simulador.simular(
            principal=1000.0,
            meses=2,
            renda=10000.0,
            sistema=SistemaAmortizacao.PRICE,
        )
        assert resultado.aprovado is True
        assert resultado.numero_parcelas == 2
        assert resultado.valor_parcela == 518.83
        assert resultado.parcelas == [518.83, 518.83]
        assert resultado.total_pago == 1037.66

    def test_simular_aprovado_sac_60_meses_faixa_maxima(self, simulador: SimuladorEmprestimo):
        """SAC no prazo máximo de 60 meses com conferência exata."""
        resultado = simulador.simular(
            principal=3000.0,
            meses=60,
            renda=10000.0,
            sistema=SistemaAmortizacao.SAC,
        )
        assert resultado.aprovado is True
        assert resultado.numero_parcelas == 60
        assert resultado.valor_parcela == 170.0  # primeira parcela
        assert resultado.parcelas[0] == 170.0
        assert resultado.parcelas[-1] == 52.0
        assert resultado.total_pago == 6660.0


# ==============================================================================
# 8. Parâmetros customizados do construtor (custom_)
# ==============================================================================


class TestConstrutorCustomizado:
    """Testes com parâmetros customizados de SimuladorEmprestimo."""

    def test_custom_taxa_base(self):
        """Customização de taxa_base afeta todas as faixas de prazo."""
        sim = SimuladorEmprestimo(taxa_base=0.05)
        assert sim.taxa_por_prazo(3) == pytest.approx(0.045)
        assert sim.taxa_por_prazo(10) == pytest.approx(0.050)
        assert sim.taxa_por_prazo(20) == pytest.approx(0.055)
        assert sim.taxa_por_prazo(40) == pytest.approx(0.060)

    def test_custom_valor_minimo(self, simulador_custom: SimuladorEmprestimo):
        """Simulador com valor_minimo=500.0 rejeita valores abaixo de 500."""
        # 499.99 deve ser rejeitado por valor_abaixo_minimo
        res_nok = simulador_custom.simular(principal=499.99, meses=12, renda=10000.0)
        assert res_nok.aprovado is False
        assert res_nok.motivo == "valor_abaixo_minimo"

        # 500.00 deve ser aceito
        res_ok = simulador_custom.simular(principal=500.0, meses=12, renda=10000.0)
        assert res_ok.aprovado is True

    def test_custom_prazo_min_e_max(self, simulador_custom: SimuladorEmprestimo):
        """Simulador com prazo_min=6 e prazo_max=36 altera as fronteiras de prazo."""
        # Prazo 5 -> prazo_curto
        res_curto = simulador_custom.simular(principal=1000.0, meses=5, renda=10000.0)
        assert res_curto.aprovado is False
        assert res_curto.motivo == "prazo_curto"

        # Prazo 6 -> aceito
        res_piso = simulador_custom.simular(principal=1000.0, meses=6, renda=10000.0)
        assert res_piso.aprovado is True

        # Prazo 36 -> aceito
        res_teto = simulador_custom.simular(principal=1000.0, meses=36, renda=10000.0)
        assert res_teto.aprovado is True

        # Prazo 37 -> prazo_longo
        res_longo = simulador_custom.simular(principal=1000.0, meses=37, renda=10000.0)
        assert res_longo.aprovado is False
        assert res_longo.motivo == "prazo_longo"

    def test_custom_teto_comprometimento(self, simulador_custom: SimuladorEmprestimo):
        """Simulador com teto_comprometimento=0.20 (20% da renda)."""
        # Renda 10000 -> Teto de empréstimo = 3000. Teto de parcela = 2000.00 (20%)
        # Com principal = 3000 e meses = 6 (taxa = 0.045):
        # Price: parcela = 3000 * 0.045 * 1.045^6 / (1.045^6 - 1) ~ 581.08 <= 2000.00 (OK)
        res = simulador_custom.simular(principal=3000.0, meses=6, renda=10000.0)
        assert res.aprovado is True
