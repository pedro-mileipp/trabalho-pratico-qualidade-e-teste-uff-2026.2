"""Testes de sistema (Selenium) da Consulta de Tarifas — RF04, issue #58.

Automatizam os casos manuais de ``tests/testes_manuais/tarifas/caso_tarifas.md`` (CT-01 a CT-15),
com o mesmo id, e acrescentam as recusas do formulário, o acesso sem login e um caso do defeito #78.

A tela ``/tarifas`` chama ``TarifaBancaria(TarifasBase()).tarifa_mensal(tipo, saldo, pacote,
transacoes)``: a antiguidade não é exposta (sempre 0), e o formulário não aceita valores negativos.
"""

from __future__ import annotations

import pytest
from pagina_tarifas import PaginaTarifas


@pytest.mark.parametrize(
    ("tipo", "saldo", "transacoes", "pacote", "tarifa"),
    [
        pytest.param("corrente", 0, 0, False, 30.00, id="ct01_corrente_zerado_sem_pacote"),
        pytest.param("poupanca", 0, 0, False, 0.00, id="ct02_poupanca_zerado_sem_pacote"),
        pytest.param("premium", 0, 0, False, 50.00, id="ct03_premium_zerado_sem_pacote"),
        pytest.param("corrente", "4999.99", 0, False, 30.00, id="ct04_corrente_um_centavo_abaixo_da_isencao"),
        pytest.param("corrente", 5000, 0, False, 0.00, id="ct05_corrente_na_fronteira_da_isencao"),
        pytest.param("premium", "49999.99", 0, False, 50.00, id="ct06_premium_um_centavo_abaixo_da_isencao"),
        pytest.param("premium", 50000, 0, False, 0.00, id="ct07_premium_na_fronteira_da_isencao"),
        pytest.param("corrente", 0, 10, False, 30.00, id="ct08_corrente_10_transacoes_na_cota"),
        pytest.param("corrente", 0, 11, False, 32.50, id="ct09_corrente_11_transacoes_primeira_excedente"),
        pytest.param("poupanca", 0, 20, False, 0.00, id="ct10_poupanca_20_transacoes"),
        pytest.param("premium", 50000, 0, True, 0.00, id="ct11_premium_pacote_isencao_total"),
        pytest.param("corrente", 5000, 0, True, 15.00, id="ct12_corrente_pacote_desconto_50"),
        pytest.param("premium", 3000, 0, True, 35.00, id="ct13_premium_pacote_desconto_30"),
        pytest.param("corrente", 0, 20, True, 30.00, id="ct14_corrente_pacote_ignora_extras"),
        pytest.param("corrente", 5000, 15, False, 12.50, id="ct15_corrente_isenta_com_transacoes_excedentes"),
    ],
)
def test_consulta_de_tarifa(
    navegador, servidor, cliente_logado, evidencia, tipo, saldo, transacoes, pacote, tarifa
):
    pagina = PaginaTarifas(navegador, servidor).abrir()
    pagina.preencher(tipo, saldo, transacoes, pacote)
    evidencia("formulario_preenchido")

    pagina.enviar()

    assert pagina.tarifa_exibida() == pytest.approx(tarifa)


@pytest.mark.parametrize(
    ("campo", "saldo", "transacoes"),
    [
        pytest.param("saldo", -100, 0, id="saldo_negativo_bloqueado"),
        pytest.param("transacoes", 0, -1, id="transacoes_negativas_bloqueadas"),
    ],
)
def test_valor_negativo_e_barrado_pelo_formulario(
    navegador, servidor, cliente_logado, evidencia, campo, saldo, transacoes
):
    pagina = PaginaTarifas(navegador, servidor).abrir()
    pagina.preencher("corrente", saldo, transacoes, pacote=False)
    evidencia("formulario_preenchido")

    pagina.enviar()

    assert pagina.campo_abaixo_do_minimo(campo)
    assert not pagina.tem_resultado()
    assert navegador.current_url == servidor + PaginaTarifas.CAMINHO


def test_tarifas_exige_login(navegador, servidor):
    navegador.get(servidor + PaginaTarifas.CAMINHO)

    assert navegador.current_url == servidor + "/login"


@pytest.mark.xfail(strict=True, reason="#78")
def test_defeito_78_pacote_premium_meia_tarifa(navegador, servidor, cliente_logado, evidencia):
    # Premium com pacote e saldo entre 5000 e 50000: a meia tarifa deveria ser a da premium
    # (50 × 0,5 = 25,00), mas a tela mostra hoje 15,00 (meia tarifa da corrente). Ver issue #78.
    pagina = PaginaTarifas(navegador, servidor).abrir()
    pagina.preencher("premium", 6000, 0, pacote=True)
    evidencia("formulario_preenchido")

    pagina.enviar()

    assert pagina.tarifa_exibida() == pytest.approx(25.00)
