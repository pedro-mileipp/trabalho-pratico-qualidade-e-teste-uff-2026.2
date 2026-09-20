from __future__ import annotations

import pytest

from app.dominio.tarifas import TarifaBancaria, TarifasBase, TipoConta


@pytest.fixture
def tarifa() -> TarifaBancaria:
    return TarifaBancaria()


@pytest.mark.parametrize(
    ("tipo", "saldo", "esperado"),
    [
        pytest.param(TipoConta.POUPANCA, 5000.0, 0.0, id="poupanca_sem_taxa"),
        pytest.param(TipoConta.CORRENTE, 1000.0, 30.0, id="corrente_sem_isencao"),
        pytest.param(TipoConta.CORRENTE, 6000.0, 0.0, id="corrente_isenta_por_saldo"),
        pytest.param(TipoConta.PREMIUM, 60000.0, 0.0, id="premium_isento_por_saldo"),
        pytest.param(TipoConta.PREMIUM, 20000.0, 50.0, id="premium_sem_isencao"),
    ],
)
def test_tarifa_mensal_sem_pacote(tipo: TipoConta, saldo: float, esperado: float, tarifa: TarifaBancaria):
    assert tarifa.tarifa_mensal(tipo, saldo) == esperado


@pytest.mark.parametrize(
    ("tipo", "saldo", "quantidade_transacoes", "antiguidade_meses", "esperado"),
    [
        pytest.param(TipoConta.CORRENTE, 3000.0, 15, 0, 42.5, id="corrente_com_transacoes_extras"),
        pytest.param(TipoConta.CORRENTE, 1000.0, 0, 40, 24.0, id="corrente_por_antiguidade_40_meses"),
        pytest.param(TipoConta.CORRENTE, -100.0, 0, 0, 36.0, id="corrente_saldo_negativo"),
        pytest.param(TipoConta.PREMIUM, 40000.0, 0, 40, 40.0, id="premium_por_antiguidade"),
        pytest.param(TipoConta.PREMIUM, 30000.0, 15, 0, 62.5, id="premium_transacoes_extras"),
    ],
)
def test_tarifa_mensal_regras_de_negocio(
    tipo: TipoConta,
    saldo: float,
    quantidade_transacoes: int,
    antiguidade_meses: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    assert (
        tarifa.tarifa_mensal(
            tipo,
            saldo,
            quantidade_transacoes=quantidade_transacoes,
            antiguidade_meses=antiguidade_meses,
        )
        == esperado
    )


@pytest.mark.parametrize(
    ("tipo", "saldo", "antiguidade_meses", "esperado"),
    [
        pytest.param(TipoConta.CORRENTE, 6000.0, 0, 15.0, id="corrente_pacote_saldo_alto"),
        pytest.param(TipoConta.CORRENTE, 3000.0, 0, 30.0, id="corrente_pacote_sem_isencao"),
        pytest.param(TipoConta.PREMIUM, 60000.0, 0, 0.0, id="premium_pacote_isento"),
        pytest.param(TipoConta.PREMIUM, 4000.0, 0, 35.0, id="premium_pacote_sem_isencao"),
        pytest.param(TipoConta.CORRENTE, 4000.0, 24, 15.0, id="corrente_pacote_antiguidade_24"),
    ],
)
def test_tarifa_mensal_com_pacote(
    tipo: TipoConta,
    saldo: float,
    antiguidade_meses: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    assert tarifa.tarifa_mensal(tipo, saldo, tem_pacote=True, antiguidade_meses=antiguidade_meses) == esperado


@pytest.mark.parametrize(
    ("quantidade", "esperado"),
    [
        pytest.param(0, 0.0, id="zero_transacoes"),
        pytest.param(10, 0.0, id="cota_gratuita"),
        pytest.param(11, 2.5, id="uma_extra"),
        pytest.param(15, 12.5, id="cinco_extras"),
    ],
)
def test_tarifa_por_transacao_extra(quantidade: int, esperado: float, tarifa: TarifaBancaria):
    assert tarifa.tarifa_por_transacao_extra(quantidade) == esperado


@pytest.mark.parametrize(
    ("tipo", "saldo", "esperado"),
    [
        pytest.param(TipoConta.CORRENTE, 6000.0, True, id="corrente_isencao"),
        pytest.param(TipoConta.CORRENTE, 4000.0, False, id="corrente_sem_isencao"),
        pytest.param(TipoConta.PREMIUM, 50000.0, True, id="premium_isencao"),
        pytest.param(TipoConta.POUPANCA, 1000.0, True, id="poupanca_isencao"),
        pytest.param(TipoConta.POUPANCA, 500.0, False, id="poupanca_sem_isencao"),
    ],
)
def test_tem_isencao(tipo: TipoConta, saldo: float, esperado: bool, tarifa: TarifaBancaria):
    assert tarifa._tem_isencao(tipo, saldo) is esperado


@pytest.mark.parametrize(
    ("tipo", "saldo", "esperado"),
    [
        pytest.param(TipoConta.CORRENTE, 3000.0, 30.0, id="corrente_sem_pacote"),
        pytest.param(TipoConta.CORRENTE, 6000.0, 30.0, id="corrente_pacote_base"),
        pytest.param(TipoConta.PREMIUM, 60000.0, 0.0, id="premium_isento"),
        pytest.param(TipoConta.PREMIUM, 4000.0, 35.0, id="premium_pacote"),
    ],
)
def test_tarifa_com_pacote(tipo: TipoConta, saldo: float, esperado: float, tarifa: TarifaBancaria):
    assert tarifa._tarifa_com_pacote(tipo, saldo) == esperado


@pytest.mark.parametrize(
    ("tipo", "saldo", "tem_pacote", "quantidade_transacoes", "esperado"),
    [
        pytest.param(TipoConta.CORRENTE, 6000.0, False, 0, 0.0, id="anual_isenta"),
        pytest.param(TipoConta.CORRENTE, 1000.0, False, 0, 360.0, id="anual_corrente_sem_isencao"),
        pytest.param(TipoConta.PREMIUM, 40000.0, False, 15, 750.0, id="anual_premium_transacoes_extras"),
    ],
)
def test_tarifa_anual(
    tipo: TipoConta,
    saldo: float,
    tem_pacote: bool,
    quantidade_transacoes: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    assert tarifa.tarifa_anual(tipo, saldo, tem_pacote, quantidade_transacoes) == esperado


def test_tarifas_base_default():
    base = TarifasBase()
    assert base.corrente == 30.0
    assert base.poupanca == 0.0
    assert base.premium == 50.0
    assert base.faixas_isencao == (1000.0, 5000.0, 50000.0)
    assert base.tarifa_por_transacao == 2.5
    assert base.transacoes_gratuitas == 10


def test_tarifas_base_personalizada():
    base = TarifasBase(corrente=35.0, premium=60.0, tarifa_por_transacao=3.0, transacoes_gratuitas=8)
    assert base.corrente == 35.0
    assert base.premium == 60.0
    assert base.tarifa_por_transacao == 3.0
    assert base.transacoes_gratuitas == 8


def test_instancia_personalizada_usa_base_recebida():
    base = TarifasBase(corrente=40.0, premium=70.0, tarifa_por_transacao=3.0, transacoes_gratuitas=5)
    tarifa = TarifaBancaria(base)

    assert tarifa._base == base
    assert tarifa.tarifa_mensal(TipoConta.CORRENTE, 1000.0) == 40.0
    assert tarifa.tarifa_por_transacao_extra(7) == 6.0


@pytest.mark.parametrize(
    ("tipo", "saldo", "tem_pacote", "quantidade_transacoes", "antiguidade_meses", "esperado"),
    [
        pytest.param(TipoConta.CORRENTE, 6000.0, True, 0, 0, 15.0, id="corrente_pacote_alto_saldo"),
        pytest.param(TipoConta.CORRENTE, 7000.0, True, 25, 0, 15.0, id="corrente_pacote_ignora_transacoes_extra"),
        pytest.param(TipoConta.PREMIUM, 50000.0, True, 0, 0, 0.0, id="premium_pacote_isencao_5x5"),
        pytest.param(TipoConta.CORRENTE, 3000.0, False, 0, 40, 24.0, id="corrente_antiguidade_e_sem_pacote"),
    ],
)
def test_tarifa_mensal_cenarios_combinados(
    tipo: TipoConta,
    saldo: float,
    tem_pacote: bool,
    quantidade_transacoes: int,
    antiguidade_meses: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    assert (
        tarifa.tarifa_mensal(
            tipo,
            saldo,
            tem_pacote=tem_pacote,
            quantidade_transacoes=quantidade_transacoes,
            antiguidade_meses=antiguidade_meses,
        )
        == esperado
    )


@pytest.mark.parametrize(
    ("quantidade", "esperado"),
    [
        pytest.param(-1, 0.0, id="quantidade_negativa"),
        pytest.param(1, 0.0, id="um_abaixo_da_cota"),
        pytest.param(11, 2.5, id="margem_exata"),
        pytest.param(12, 5.0, id="duas_extras"),
        pytest.param(20, 25.0, id="muito_acima_da_cota"),
    ],
)
def test_tarifa_por_transacao_extra_borda(quantidade: int, esperado: float, tarifa: TarifaBancaria):
    assert tarifa.tarifa_por_transacao_extra(quantidade) == esperado


@pytest.mark.parametrize(
    ("tipo", "saldo", "tem_pacote", "quantidade_transacoes", "esperado"),
    [
        pytest.param(TipoConta.POUPANCA, 999.0, False, 0, 0.0, id="poupanca_abaixo_da_isencao"),
        pytest.param(TipoConta.CORRENTE, 999.0, False, 0, 30.0, id="corrente_abaixo_isencao"),
        pytest.param(TipoConta.CORRENTE, 5000.0, False, 10, 0.0, id="corrente_faixa_limite_exato"),
        pytest.param(TipoConta.CORRENTE, 5000.0, False, 11, 2.5, id="corrente_limite_exato_mais_um"),
        pytest.param(TipoConta.PREMIUM, 50000.0, False, 0, 0.0, id="premium_limite_exato"),
    ],
)
def test_tarifa_mensal_valor_limite(
    tipo: TipoConta,
    saldo: float,
    tem_pacote: bool,
    quantidade_transacoes: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    assert (
        tarifa.tarifa_mensal(
            tipo,
            saldo,
            tem_pacote=tem_pacote,
            quantidade_transacoes=quantidade_transacoes,
        )
        == esperado
    )
