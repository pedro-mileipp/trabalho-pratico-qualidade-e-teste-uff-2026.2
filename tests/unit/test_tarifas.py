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
    ("tipo", "saldo", "quantidade_transacoes", "esperado"),
    [
        pytest.param(TipoConta.CORRENTE, 3000.0, 15, 42.5, id="corrente_com_transacoes_extras"),
        pytest.param(TipoConta.CORRENTE, -100.0, 0, 36.0, id="corrente_saldo_negativo"),
        pytest.param(TipoConta.PREMIUM, 30000.0, 15, 62.5, id="premium_transacoes_extras"),
    ],
)
def test_tarifa_mensal_regras_de_negocio(
    tipo: TipoConta,
    saldo: float,
    quantidade_transacoes: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    assert (
        tarifa.tarifa_mensal(
            tipo,
            saldo,
            quantidade_transacoes=quantidade_transacoes,
        )
        == esperado
    )


@pytest.mark.parametrize(
    ("tipo", "saldo", "esperado"),
    [
        pytest.param(TipoConta.CORRENTE, 6000.0, 15.0, id="corrente_pacote_saldo_alto"),
        pytest.param(TipoConta.CORRENTE, 3000.0, 30.0, id="corrente_pacote_sem_isencao"),
        pytest.param(TipoConta.PREMIUM, 60000.0, 0.0, id="premium_pacote_isento"),
        pytest.param(TipoConta.PREMIUM, 4000.0, 35.0, id="premium_pacote_sem_isencao"),
    ],
)
def test_tarifa_mensal_com_pacote(
    tipo: TipoConta,
    saldo: float,
    esperado: float,
    tarifa: TarifaBancaria,
):
    assert tarifa.tarifa_mensal(tipo, saldo, tem_pacote=True) == esperado


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
    ("tipo", "saldo", "tem_pacote", "quantidade_transacoes", "esperado"),
    [
        pytest.param(TipoConta.CORRENTE, 6000.0, True, 0, 15.0, id="corrente_pacote_alto_saldo"),
        pytest.param(TipoConta.CORRENTE, 7000.0, True, 25, 15.0, id="corrente_pacote_ignora_transacoes_extra"),
        pytest.param(TipoConta.PREMIUM, 50000.0, True, 0, 0.0, id="premium_pacote_isento_saldo_limite_50000"),
    ],
)
def test_tarifa_mensal_cenarios_combinados(
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


# ---------------------------------------------------------------------------
# Entrega 2 — issue #40: técnicas funcionais e cobertura estrutural
#
# Prefixo do id de cada caso = técnica que o gerou:
#   pe_     partição de equivalência
#   vl_     análise de valor-limite
#   td_     tabela de decisão de tarifa_mensal (regras R1..R8)
#   custom_ parâmetros personalizados de TarifasBase
# Teste de laços: não se aplica, TarifaBancaria não possui laços.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("tipo", "saldo", "tem_pacote", "quantidade_transacoes", "antiguidade_meses", "esperado"),
    [
        pytest.param(TipoConta.POUPANCA, -500.0, True, 20, 50, 0.0, id="pe_poupanca_sempre_gratuita"),
        pytest.param(TipoConta.CORRENTE, 2500.0, False, 0, -12, 30.0, id="pe_antiguidade_negativa_sem_validacao"),
        pytest.param(TipoConta.CORRENTE, 2500.0, False, 0, 0, 30.0, id="pe_corrente_antiguidade_nova"),
        pytest.param(TipoConta.CORRENTE, 2500.0, False, 0, 12, 30.0, id="pe_corrente_antiguidade_media"),
        pytest.param(TipoConta.CORRENTE, 2500.0, False, 0, 60, 24.0, id="pe_corrente_antiguidade_alta"),
        pytest.param(TipoConta.PREMIUM, 20000.0, False, 0, 60, 40.0, id="pe_premium_antiguidade_alta"),
        pytest.param(TipoConta.PREMIUM, -100.0, False, 0, 0, 56.0, id="pe_premium_saldo_negativo"),
        pytest.param(TipoConta.CORRENTE, 1000.0, True, 0, 30, 15.0, id="pe_corrente_pacote_antiguidade_media"),
        # tipo de conta x pacote x saldo (negativo / zero / positivo): combinações ainda não cobertas
        pytest.param(TipoConta.POUPANCA, -100.0, False, 0, 0, 0.0, id="pe_poupanca_sem_pacote_saldo_negativo"),
        pytest.param(TipoConta.POUPANCA, 0.0, False, 0, 0, 0.0, id="pe_poupanca_sem_pacote_saldo_zero"),
        pytest.param(TipoConta.PREMIUM, 0.0, False, 0, 0, 50.0, id="pe_premium_sem_pacote_saldo_zero"),
        pytest.param(TipoConta.CORRENTE, -100.0, True, 0, 0, 30.0, id="pe_corrente_pacote_saldo_negativo"),
        pytest.param(TipoConta.CORRENTE, 0.0, True, 0, 0, 30.0, id="pe_corrente_pacote_saldo_zero"),
        pytest.param(TipoConta.POUPANCA, 0.0, True, 0, 0, 0.0, id="pe_poupanca_pacote_saldo_zero"),
        pytest.param(TipoConta.POUPANCA, 2000.0, True, 0, 0, 0.0, id="pe_poupanca_pacote_saldo_positivo"),
        pytest.param(TipoConta.PREMIUM, -100.0, True, 0, 0, 35.0, id="pe_premium_pacote_saldo_negativo"),
        pytest.param(TipoConta.PREMIUM, 0.0, True, 0, 0, 35.0, id="pe_premium_pacote_saldo_zero"),
    ],
)
def test_tarifa_mensal_particao_equivalencia(
    tipo: TipoConta,
    saldo: float,
    tem_pacote: bool,
    quantidade_transacoes: int,
    antiguidade_meses: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    resultado = tarifa.tarifa_mensal(
        tipo,
        saldo,
        tem_pacote=tem_pacote,
        quantidade_transacoes=quantidade_transacoes,
        antiguidade_meses=antiguidade_meses,
    )
    assert resultado == esperado


@pytest.mark.parametrize(
    ("tipo", "saldo", "tem_pacote", "quantidade_transacoes", "antiguidade_meses", "esperado"),
    [
        # desconto de 20% por antiguidade, sem pacote (limite 36 meses) — linha 49
        pytest.param(TipoConta.CORRENTE, 1000.0, False, 0, 35, 30.0, id="vl_antiguidade_35_sem_desconto"),
        pytest.param(TipoConta.CORRENTE, 1000.0, False, 0, 36, 24.0, id="vl_antiguidade_36_com_desconto"),
        pytest.param(TipoConta.CORRENTE, 1000.0, False, 0, 37, 24.0, id="vl_antiguidade_37_com_desconto"),
        pytest.param(TipoConta.PREMIUM, 20000.0, False, 0, 35, 50.0, id="vl_premium_antiguidade_35"),
        pytest.param(TipoConta.PREMIUM, 20000.0, False, 0, 36, 40.0, id="vl_premium_antiguidade_36"),
        # meia tarifa no pacote por antiguidade (limite 24 meses)
        pytest.param(TipoConta.CORRENTE, 1000.0, True, 0, 23, 30.0, id="vl_pacote_antiguidade_23"),
        pytest.param(TipoConta.CORRENTE, 1000.0, True, 0, 24, 15.0, id="vl_pacote_antiguidade_24"),
        pytest.param(TipoConta.CORRENTE, 1000.0, True, 0, 25, 15.0, id="vl_pacote_antiguidade_25"),
        # meia tarifa no pacote por saldo (limite 5000)
        pytest.param(TipoConta.CORRENTE, 4999.99, True, 0, 0, 30.0, id="vl_pacote_saldo_4999_99"),
        pytest.param(TipoConta.CORRENTE, 5000.0, True, 0, 0, 15.0, id="vl_pacote_saldo_5000"),
        # isenção por saldo sem pacote (corrente 5000, premium 50000)
        pytest.param(TipoConta.CORRENTE, 4999.99, False, 0, 0, 30.0, id="vl_corrente_saldo_4999_99"),
        pytest.param(TipoConta.CORRENTE, 5000.01, False, 0, 0, 0.0, id="vl_corrente_saldo_5000_01"),
        pytest.param(TipoConta.PREMIUM, 49999.99, False, 0, 0, 50.0, id="vl_premium_saldo_49999_99"),
        # faixa de isenção da poupança (1000): tarifa_mensal retorna 0 antes de consultá-la
        pytest.param(TipoConta.POUPANCA, 999.99, False, 0, 0, 0.0, id="vl_poupanca_mensal_999_99"),
        pytest.param(TipoConta.POUPANCA, 1000.0, False, 0, 0, 0.0, id="vl_poupanca_mensal_1000"),
        # sobretaxa de saldo negativo (limite 0)
        pytest.param(TipoConta.CORRENTE, -0.01, False, 0, 0, 36.0, id="vl_saldo_menos_0_01_sobretaxa"),
        pytest.param(TipoConta.CORRENTE, 0.0, False, 0, 0, 30.0, id="vl_saldo_zero_sem_sobretaxa"),
        # cota de transações combinada com o desconto por antiguidade
        pytest.param(TipoConta.CORRENTE, 1000.0, False, 9, 36, 24.0, id="vl_antiguidade_36_9_transacoes"),
        pytest.param(TipoConta.CORRENTE, 1000.0, False, 10, 36, 24.0, id="vl_antiguidade_36_10_transacoes"),
        pytest.param(TipoConta.CORRENTE, 1000.0, False, 11, 36, 26.5, id="vl_antiguidade_36_11_transacoes"),
        pytest.param(TipoConta.CORRENTE, -100.0, False, 11, 0, 38.5, id="vl_saldo_negativo_11_transacoes"),
    ],
)
def test_tarifa_mensal_valor_limite_antiguidade_e_saldo(
    tipo: TipoConta,
    saldo: float,
    tem_pacote: bool,
    quantidade_transacoes: int,
    antiguidade_meses: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    resultado = tarifa.tarifa_mensal(
        tipo,
        saldo,
        tem_pacote=tem_pacote,
        quantidade_transacoes=quantidade_transacoes,
        antiguidade_meses=antiguidade_meses,
    )
    assert resultado == esperado


@pytest.mark.parametrize(
    ("tipo", "saldo", "esperado"),
    [
        pytest.param(TipoConta.POUPANCA, 999.99, False, id="vl_poupanca_999_99"),
        pytest.param(TipoConta.CORRENTE, 4999.99, False, id="vl_corrente_4999_99"),
        pytest.param(TipoConta.CORRENTE, 5000.0, True, id="vl_corrente_5000"),
        pytest.param(TipoConta.PREMIUM, 49999.99, False, id="vl_premium_49999_99"),
    ],
)
def test_tem_isencao_valor_limite(tipo: TipoConta, saldo: float, esperado: bool, tarifa: TarifaBancaria):
    assert tarifa._tem_isencao(tipo, saldo) is esperado


# Tabela de decisão de tarifa_mensal (condições na ordem em que o código as avalia):
#   R1 poupança                                            -> 0
#   R2 pacote, premium com saldo >= 50000                  -> 0
#   R3 pacote, saldo >= 5000 ou antiguidade >= 24          -> corrente * 0,5
#   R4 pacote, demais casos                                -> corrente 30 / premium 35
#   R5 sem pacote, isenção por saldo                       -> 0 + extras
#   R6 sem pacote, sem isenção, antiguidade >= 36          -> base * 0,8 + extras
#   R7 sem pacote, sem isenção, antig. < 36, saldo < 0     -> base + corrente * 0,2 + extras
#   R8 sem pacote, demais casos                            -> base + extras
#
# Tabela 1 — sem pacote (conta corrente, base 30,00): combinações de
#   C1 isenção por saldo (saldo >= 5000)  x  C2 antiguidade >= 36  x
#   C3 saldo negativo  x  C4 transações extras (12 transações = +5,00).
# C1 e C3 são mutuamente exclusivas (saldo >= 5000 não é negativo): 12 combinações possíveis.
# Precedência do if/elif: isenção > antiguidade > saldo negativo; as extras somam em todas.
# As linhas td_sp_premium_* repetem regras da tabela na conta premium (base 50,00, isenção a
# partir de 50000), onde a sobretaxa de saldo negativo continua sendo corrente * 0,2.
# Algumas linhas coincidem com casos vl_/Entrega 1: mantidas para a tabela ficar completa.
@pytest.mark.parametrize(
    ("tipo", "saldo", "antiguidade_meses", "quantidade_transacoes", "esperado"),
    [
        #                                                                                       C1  C2  C3  C4
        pytest.param(TipoConta.CORRENTE, 6000.0, 0, 0, 0.0, id="td_sp_01_isento"),                              # V F F F
        pytest.param(TipoConta.CORRENTE, 6000.0, 0, 12, 5.0, id="td_sp_02_isento_extras"),                      # V F F V
        pytest.param(TipoConta.CORRENTE, 6000.0, 36, 0, 0.0, id="td_sp_03_isento_antiguidade"),                 # V V F F
        pytest.param(TipoConta.CORRENTE, 6000.0, 36, 12, 5.0, id="td_sp_04_isento_antiguidade_extras"),         # V V F V
        pytest.param(TipoConta.CORRENTE, 1000.0, 0, 0, 30.0, id="td_sp_05_nenhuma_condicao"),                   # F F F F
        pytest.param(TipoConta.CORRENTE, 1000.0, 0, 12, 35.0, id="td_sp_06_extras"),                            # F F F V
        pytest.param(TipoConta.CORRENTE, 1000.0, 36, 0, 24.0, id="td_sp_07_antiguidade"),                       # F V F F
        pytest.param(TipoConta.CORRENTE, 1000.0, 36, 12, 29.0, id="td_sp_08_antiguidade_extras"),               # F V F V
        pytest.param(TipoConta.CORRENTE, -100.0, 0, 0, 36.0, id="td_sp_09_negativo"),                           # F F V F
        pytest.param(TipoConta.CORRENTE, -100.0, 0, 12, 41.0, id="td_sp_10_negativo_extras"),                   # F F V V
        pytest.param(TipoConta.CORRENTE, -100.0, 36, 0, 24.0, id="td_sp_11_antiguidade_prevalece_negativo"),    # F V V F
        pytest.param(TipoConta.CORRENTE, -100.0, 36, 12, 29.0, id="td_sp_12_antiguidade_prevalece_negativo_extras"),  # F V V V
        # premium: 50000 isento mesmo com antiguidade; 50*0,8 = 40; 40 + 5*2,50 = 52,50
        pytest.param(TipoConta.PREMIUM, 50000.0, 36, 0, 0.0, id="td_sp_premium_isento_limite_com_antiguidade"),
        pytest.param(TipoConta.PREMIUM, -100.0, 36, 0, 40.0, id="td_sp_premium_antiguidade_prevalece_negativo"),
        pytest.param(TipoConta.PREMIUM, 20000.0, 36, 15, 52.5, id="td_sp_premium_antiguidade_extras"),
    ],
)
def test_tarifa_mensal_tabela_decisao_sem_pacote(
    tipo: TipoConta,
    saldo: float,
    antiguidade_meses: int,
    quantidade_transacoes: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    resultado = tarifa.tarifa_mensal(
        tipo,
        saldo,
        quantidade_transacoes=quantidade_transacoes,
        antiguidade_meses=antiguidade_meses,
    )
    assert resultado == esperado


# Tabela 2 — com pacote: combinações de
#   tipo (corrente / premium)  x  saldo >= 50000  x  saldo >= 5000  x  antiguidade >= 24.
# saldo >= 50000 implica saldo >= 5000, então há 3 faixas de saldo (1000 / 20000 / 60000):
# 2 tipos x 3 faixas x 2 antiguidades = 12 combinações. Poupança decide antes (R1).
# As 3 combinações premium da regra R3 estão no teste do defeito #78.
@pytest.mark.parametrize(
    ("tipo", "saldo", "antiguidade_meses", "quantidade_transacoes", "esperado"),
    [
        pytest.param(TipoConta.POUPANCA, -100.0, 40, 20, 0.0, id="td_cp_r1_poupanca_prevalece_sobre_tudo"),
        pytest.param(TipoConta.CORRENTE, 1000.0, 0, 0, 30.0, id="td_cp_corrente_1000_antig_0"),
        pytest.param(TipoConta.CORRENTE, 1000.0, 24, 0, 15.0, id="td_cp_corrente_1000_antig_24"),
        pytest.param(TipoConta.CORRENTE, 20000.0, 0, 0, 15.0, id="td_cp_corrente_20000_antig_0"),
        pytest.param(TipoConta.CORRENTE, 20000.0, 24, 0, 15.0, id="td_cp_corrente_20000_antig_24"),
        pytest.param(TipoConta.CORRENTE, 60000.0, 0, 0, 15.0, id="td_cp_corrente_60000_sem_isencao_total"),
        pytest.param(TipoConta.CORRENTE, 60000.0, 24, 0, 15.0, id="td_cp_corrente_60000_antig_24"),
        pytest.param(TipoConta.PREMIUM, 1000.0, 0, 0, 35.0, id="td_cp_premium_1000_antig_0"),
        pytest.param(TipoConta.PREMIUM, 60000.0, 0, 0, 0.0, id="td_cp_premium_60000_isento"),
        pytest.param(TipoConta.PREMIUM, 60000.0, 24, 0, 0.0, id="td_cp_premium_60000_isento_prevalece_antiguidade"),
        pytest.param(TipoConta.CORRENTE, 1000.0, 24, 20, 15.0, id="td_cp_pacote_ignora_transacoes"),
    ],
)
def test_tarifa_mensal_tabela_decisao_com_pacote(
    tipo: TipoConta,
    saldo: float,
    antiguidade_meses: int,
    quantidade_transacoes: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    resultado = tarifa.tarifa_mensal(
        tipo,
        saldo,
        tem_pacote=True,
        quantidade_transacoes=quantidade_transacoes,
        antiguidade_meses=antiguidade_meses,
    )
    assert resultado == esperado


@pytest.mark.parametrize(
    ("tipo", "saldo", "tem_pacote", "quantidade_transacoes", "esperado"),
    [
        pytest.param(TipoConta.POUPANCA, 100.0, False, 30, 0.0, id="pe_anual_poupanca"),
        # 15,00 * 12
        pytest.param(TipoConta.CORRENTE, 6000.0, True, 0, 180.0, id="pe_anual_corrente_pacote_meia_tarifa"),
        # 35,00 * 12
        pytest.param(TipoConta.PREMIUM, 4000.0, True, 0, 420.0, id="pe_anual_premium_pacote"),
        # (30 + 6 + 2,50) * 12 = 38,50 * 12
        pytest.param(TipoConta.CORRENTE, -100.0, False, 11, 462.0, id="pe_anual_saldo_negativo_com_extra"),
    ],
)
def test_tarifa_anual_particao_equivalencia(
    tipo: TipoConta,
    saldo: float,
    tem_pacote: bool,
    quantidade_transacoes: int,
    esperado: float,
    tarifa: TarifaBancaria,
):
    assert tarifa.tarifa_anual(tipo, saldo, tem_pacote, quantidade_transacoes) == esperado


def test_custom_desconto_antiguidade_usa_base_personalizada():
    tarifa = TarifaBancaria(TarifasBase(corrente=40.0))
    assert tarifa.tarifa_mensal(TipoConta.CORRENTE, 1000.0, antiguidade_meses=36) == 32.0


def test_custom_sobretaxa_premium_usa_tarifa_da_corrente():
    tarifa = TarifaBancaria(TarifasBase(corrente=40.0, premium=70.0))
    assert tarifa.tarifa_mensal(TipoConta.PREMIUM, -1.0) == 78.0


# --- Defeitos revelados (issue #40) -> bugs #77 e #78 -----------------------
# Os casos abaixo afirmam o comportamento esperado pela especificação
# (docs/aplicacao.md, seção 4.3). Falham com o código atual e ficam marcados
# como xfail(strict=True) até a correção, para não bloquear o mutmut (#45).
# Ao corrigir o defeito, remova o xfail (strict=True acusa XPASS).


@pytest.mark.xfail(strict=True, raises=TypeError, reason="#77: tarifa_anual não repassa antiguidade_meses")
def test_defeito_tarifa_anual_aplica_desconto_por_antiguidade(tarifa: TarifaBancaria):
    # mensal com 36 meses = 30 * 0,8 = 24,00 -> anual = 24 * 12 = 288,00
    assert tarifa.tarifa_anual(TipoConta.CORRENTE, 1000.0, antiguidade_meses=36) == 288.0


@pytest.mark.xfail(strict=True, reason="#78: meia tarifa do pacote premium usa a tarifa da corrente")
@pytest.mark.parametrize(
    ("saldo", "antiguidade_meses"),
    [
        pytest.param(20000.0, 0, id="td_r3_premium_saldo_20000"),
        pytest.param(1000.0, 24, id="td_r3_premium_antiguidade_24"),
        pytest.param(20000.0, 24, id="td_r3_premium_saldo_20000_antiguidade_24"),
    ],
)
def test_defeito_pacote_premium_meia_tarifa_da_premium(
    saldo: float, antiguidade_meses: int, tarifa: TarifaBancaria
):
    # meia tarifa da premium = 50 * 0,5 = 25,00 (o código devolve corrente * 0,5 = 15,00)
    assert (
        tarifa.tarifa_mensal(TipoConta.PREMIUM, saldo, tem_pacote=True, antiguidade_meses=antiguidade_meses)
        == 25.0
    )
