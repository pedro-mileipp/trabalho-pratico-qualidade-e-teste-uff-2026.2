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