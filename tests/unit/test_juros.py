from __future__ import annotations

import pytest

from app.dominio.juros import CalculadoraJuros, TabelaTaxas


@pytest.fixture
def calc() -> CalculadoraJuros:
    return CalculadoraJuros()


@pytest.mark.parametrize(
    ("meses", "esperado"),
    [
        pytest.param(1, 0.12, id="faixa1_inicio"),
        pytest.param(6, 0.12, id="faixa1_limite_exato"),
        pytest.param(7, 0.18, id="faixa2_inicio"),
        pytest.param(12, 0.18, id="faixa2_limite_exato"),
        pytest.param(13, 0.24, id="faixa3_inicio"),
        pytest.param(24, 0.24, id="faixa3_limite_exato"),
        pytest.param(25, 0.30, id="faixa4_inicio"),
        pytest.param(36, 0.30, id="faixa4_limite_exato"),
        pytest.param(48, 0.30, id="faixa_acima_do_maximo"),
    ],
)
def test_taxa_para_prazo_faixas(calc: CalculadoraJuros, meses: int, esperado: float):
    assert calc.taxa_para_prazo(meses) == esperado


def test_taxa_para_prazo_tabela_customizada():
    tabela = TabelaTaxas([(5, 0.05), (10, 0.10)])
    calc_custom = CalculadoraJuros(tabela=tabela)
    assert calc_custom.taxa_para_prazo(3) == 0.05
    assert calc_custom.taxa_para_prazo(10) == 0.10
    assert calc_custom.taxa_para_prazo(15) == 0.10


@pytest.mark.parametrize(
    ("taxa_anual", "esperado"),
    [
        pytest.param(0.12, 0.009488792934583046, id="taxa_positiva_12_porcento"),
        pytest.param(0.0, 0.0, id="taxa_zero"),
        pytest.param(-0.05, 0.0, id="taxa_negativa"),
    ],
)
def test_taxa_mensal(calc: CalculadoraJuros, taxa_anual: float, esperado: float):
    assert pytest.approx(calc.taxa_mensal(taxa_anual), rel=1e-5) == esperado


@pytest.mark.parametrize(
    ("principal", "meses", "taxa_anual", "esperado"),
    [
        pytest.param(0, 12, 0.10, 0.0, id="principal_zero"),
        pytest.param(-1000, 12, 0.10, 0.0, id="principal_negativo"),
        pytest.param(1000, 0, 0.10, 1000.0, id="meses_zero"),
        pytest.param(1000, -5, 0.10, 1000.0, id="meses_negativo"),
        pytest.param(1000, 6, None, 1058.30, id="montante_com_taxa_padrao_faixa"),
        pytest.param(1000, 12, 0.10, 1100.0, id="montante_com_taxa_explicitada"),
    ],
)
def test_calcular_montante(
    calc: CalculadoraJuros, principal: float, meses: int, taxa_anual: float | None, esperado: float
):
    assert calc.calcular_montante(principal, meses, taxa_anual) == esperado


@pytest.mark.parametrize(
    ("valor", "dias_atraso", "esperado"),
    [
        pytest.param(0, 10, 0.0, id="valor_zero"),
        pytest.param(-100, 10, 0.0, id="valor_negativo"),
        pytest.param(1000, 0, 0.0, id="dias_zero"),
        pytest.param(1000, -5, 0.0, id="dias_negativo"),
        pytest.param(1000, 1, 20.20, id="multa_2_porcento_inicio"),
        pytest.param(1000, 15, 23.00, id="multa_2_porcento_limite"),
        pytest.param(1000, 16, 53.20, id="multa_5_porcento_inicio"),
        pytest.param(1000, 60, 62.00, id="multa_5_porcento_limite"),
        pytest.param(1000, 61, 112.20, id="multa_10_porcento_inicio"),
    ],
)
def test_juros_de_mora(calc: CalculadoraJuros, valor: float, dias_atraso: int, esperado: float):
    assert calc.juros_de_mora(valor, dias_atraso) == esperado


def test_total_a_pagar(calc: CalculadoraJuros):
    total = calc.total_a_pagar(1000, 6, dias_atraso=20)
    assert total == 1115.45


@pytest.mark.parametrize(
    ("principal", "aporte", "meses", "taxa", "cap_aporte", "ir", "esperado"),
    [
        pytest.param(0, 100, 12, 0.10, True, 0.0, 0.0, id="principal_invalido"),
        pytest.param(1000, 100, 0, 0.10, True, 0.0, 1000.0, id="meses_zerados"),
        pytest.param(1000, -10, 12, 0.10, True, 0.0, 1000.0, id="aporte_negativo"),
        pytest.param(1000, 100, 12, 0.0, True, 0.0, 2200.0, id="taxa_zero_soma_simples"),
    ],
)
def test_montante_com_aportes_casos_base(
    calc: CalculadoraJuros,
    principal: float,
    aporte: float,
    meses: int,
    taxa: float,
    cap_aporte: bool,
    ir: float,
    esperado: float,
):
    assert calc.montante_com_aportes(principal, aporte, meses, taxa, cap_aporte, ir) == esperado


def test_montante_com_aportes_capitalizacao_diferenca(calc: CalculadoraJuros):
    com_cap = calc.montante_com_aportes(1000, 100, 6, 0.10, capitaliza_aporte=True)
    sem_cap = calc.montante_com_aportes(1000, 100, 6, 0.10, capitaliza_aporte=False)
    assert com_cap > sem_cap


def test_montante_com_aportes_desconto_ir_no_mes_12(calc: CalculadoraJuros):
    com_ir = calc.montante_com_aportes(1000, 100, 12, 0.10, aliquota_ir=0.15)
    sem_ir = calc.montante_com_aportes(1000, 100, 12, 0.10, aliquota_ir=0.0)
    assert com_ir < sem_ir


def test_montante_com_aportes_trava_um_milhao(calc: CalculadoraJuros):
    resultado = calc.montante_com_aportes(1_500_000, 1000, 1, 0.10)
    rendimento_bruto = (1_500_000 + 1000) * (1 + calc.taxa_mensal(0.10))
    assert resultado < rendimento_bruto


# ---------------------------------------------------------------------------
# Novas coberturas: Partição de Equivalência (pe_), Valor-Limite (vl_),
# Tabela de Decisão (td_) e Teste de Laços (laco_).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("meses", "esperado"),
    [
        # Partição de equivalência (pe_)
        pytest.param(3, 0.12, id="pe_prazo_curto_ate_6m"),
        pytest.param(9, 0.18, id="pe_prazo_medio_7_a_12m"),
        pytest.param(18, 0.24, id="pe_prazo_longo_13_a_24m"),
        pytest.param(30, 0.30, id="pe_prazo_estendido_25_a_36m"),
        pytest.param(60, 0.30, id="pe_prazo_muito_longo_acima_36m"),
        # Análise de valor-limite (vl_)
        pytest.param(-1, 0.12, id="vl_prazo_negativo_cai_primeira_faixa"),
        pytest.param(0, 0.12, id="vl_prazo_zero_cai_primeira_faixa"),
    ],
)
def test_taxa_para_prazo_pe_e_vl(calc: CalculadoraJuros, meses: int, esperado: float):
    assert calc.taxa_para_prazo(meses) == esperado


@pytest.mark.parametrize(
    ("principal", "meses", "dias_atraso", "taxa_anual", "esperado"),
    [
        # Partição de equivalência (pe_)
        pytest.param(1000.0, 6, 0, 0.10, 1048.81, id="pe_total_sem_atraso"),
        pytest.param(2000.0, 12, 10, 0.12, 2289.28, id="pe_total_atraso_leve_10d"),
        pytest.param(2000.0, 12, 45, 0.12, 2372.16, id="pe_total_atraso_moderado_45d"),
        pytest.param(2000.0, 12, 90, 0.12, 2504.32, id="pe_total_atraso_grave_90d"),
        # Análise de valor-limite (vl_)
        pytest.param(1000.0, 6, 15, None, 1082.64, id="vl_total_mora_limite_15d"),
        pytest.param(1000.0, 6, 16, None, 1114.60, id="vl_total_mora_limite_16d"),
        pytest.param(1000.0, 6, 60, None, 1123.91, id="vl_total_mora_limite_60d"),
        pytest.param(1000.0, 6, 61, None, 1177.04, id="vl_total_mora_limite_61d"),
    ],
)
def test_total_a_pagar_pe_e_vl(
    calc: CalculadoraJuros,
    principal: float,
    meses: int,
    dias_atraso: int,
    taxa_anual: float | None,
    esperado: float,
):
    assert calc.total_a_pagar(principal, meses, dias_atraso, taxa_anual) == esperado


@pytest.mark.parametrize(
    ("principal", "aporte", "meses", "taxa", "cap_aporte", "ir", "validador"),
    [
        # R1: capitaliza=True, sem IR, abaixo de 1M
        pytest.param(
            1000.0,
            100.0,
            3,
            0.12,
            True,
            0.0,
            lambda r, c: r
            == round(
                (((1000.0 + 100.0) * (1 + c.taxa_mensal(0.12)) + 100.0) * (1 + c.taxa_mensal(0.12)) + 100.0)
                * (1 + c.taxa_mensal(0.12)),
                2,
            ),
            id="td_r1_cap_true_sem_ir_abaixo_1m",
        ),
        # R2: capitaliza=False, sem IR, abaixo de 1M
        pytest.param(
            1000.0,
            100.0,
            2,
            0.12,
            False,
            0.0,
            lambda r, c: r == round((1000.0 * (1 + c.taxa_mensal(0.12)) + 100.0) * (1 + c.taxa_mensal(0.12)) + 100.0, 2),
            id="td_r2_cap_false_sem_ir_abaixo_1m",
        ),
        # R3: capitaliza=True, com IR no mês 12, abaixo de 1M
        pytest.param(
            1000.0,
            100.0,
            12,
            0.10,
            True,
            0.15,
            lambda r, _: 0 < r < 2300.0,
            id="td_r3_cap_true_com_ir_m12_abaixo_1m",
        ),
        # R4: capitaliza=False, com IR no mês 12, abaixo de 1M
        pytest.param(
            1000.0,
            100.0,
            12,
            0.10,
            False,
            0.15,
            lambda r, c: r < c.montante_com_aportes(1000.0, 100.0, 12, 0.10, False, 0.0),
            id="td_r4_cap_false_com_ir_m12_abaixo_1m",
        ),
        # R5: capitaliza=True, sem IR, acima de 1M (ativa trava 0.999)
        pytest.param(
            900_000.0,
            50_000.0,
            3,
            0.12,
            True,
            0.0,
            lambda r, _: r < 1_100_000.0 and r > 900_000.0,
            id="td_r5_cap_true_sem_ir_acima_1m",
        ),
        # R6: capitaliza=True, com IR no mês 12 e acima de 1M
        pytest.param(
            950_000.0,
            20_000.0,
            12,
            0.12,
            True,
            0.15,
            lambda r, c: r < c.montante_com_aportes(950_000.0, 20_000.0, 12, 0.12, True, 0.0),
            id="td_r6_cap_true_com_ir_e_acima_1m",
        ),
    ],
)
def test_montante_com_aportes_tabela_decisao(
    calc: CalculadoraJuros,
    principal: float,
    aporte: float,
    meses: int,
    taxa: float,
    cap_aporte: bool,
    ir: float,
    validador,
):
    resultado = calc.montante_com_aportes(principal, aporte, meses, taxa, cap_aporte, ir)
    assert validador(resultado, calc)


@pytest.mark.parametrize(
    ("meses", "esperado"),
    [
        # Diferentes quantidades de iterações (laco_) em calcular_montante
        pytest.param(1, 1009.49, id="laco_montante_1_iteracao"),
        pytest.param(3, 1028.74, id="laco_montante_3_iteracoes"),
        pytest.param(13, 1262.43, id="laco_montante_13_iteracoes_acima_12m"),
        pytest.param(24, 1537.60, id="laco_montante_24_iteracoes_dois_anos"),
        pytest.param(36, 2197.00, id="laco_montante_36_iteracoes_tres_anos"),
    ],
)
def test_calcular_montante_lacos(calc: CalculadoraJuros, meses: int, esperado: float):
    assert calc.calcular_montante(1000.0, meses, taxa_anual=None) == esperado


@pytest.mark.parametrize(
    ("meses", "ir", "comparador"),
    [
        # Prazos < 12m (0 ciclos de IR), = 12m (1 ciclo de IR), > 12m (1 ou 2 ciclos de IR)
        pytest.param(1, 0.15, lambda com_ir, sem_ir: com_ir == sem_ir, id="laco_aportes_1m_sem_ciclo_ir"),
        pytest.param(6, 0.15, lambda com_ir, sem_ir: com_ir == sem_ir, id="laco_aportes_6m_sem_ciclo_ir"),
        pytest.param(13, 0.15, lambda com_ir, sem_ir: com_ir < sem_ir, id="laco_aportes_13m_um_ciclo_ir_no_m12"),
        pytest.param(18, 0.15, lambda com_ir, sem_ir: com_ir < sem_ir, id="laco_aportes_18m_acima_12m_com_ir"),
        pytest.param(24, 0.15, lambda com_ir, sem_ir: com_ir < sem_ir, id="laco_aportes_24m_dois_ciclos_ir"),
    ],
)
def test_montante_com_aportes_lacos_prazos_longos(
    calc: CalculadoraJuros, meses: int, ir: float, comparador
):
    com_ir = calc.montante_com_aportes(1000.0, 100.0, meses, 0.10, capitaliza_aporte=True, aliquota_ir=ir)
    sem_ir = calc.montante_com_aportes(1000.0, 100.0, meses, 0.10, capitaliza_aporte=True, aliquota_ir=0.0)
    assert comparador(com_ir, sem_ir)


def test_montante_com_aportes_vl_trava_um_milhao_estrita(calc: CalculadoraJuros):
    # Valor-limite (vl_): abaixo de 1_000_000 no laço não sofre redução de 0.999
    sem_trava = calc.montante_com_aportes(500_000.0, 0.0, 1, 0.12, capitaliza_aporte=True, aliquota_ir=0.0)
    assert sem_trava == round(500_000.0 * (1 + calc.taxa_mensal(0.12)), 2)

    # Acima de 1_000_000 no laço sofre aplicação do multiplicador 0.999
    com_trava = calc.montante_com_aportes(1_000_001.0, 0.0, 1, 0.12, capitaliza_aporte=True, aliquota_ir=0.0)
    assert com_trava == round(round(1_000_001.0 * (1 + calc.taxa_mensal(0.12)), 2) * 0.999, 2)