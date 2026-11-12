"""Testes unitários de DecisorCredito (app/dominio/credito.py).

Técnica de cada caso, indicada pelo prefixo do id do ``pytest.param``:
    pe_     partição de equivalência
    vl_     análise de valor-limite
    td_     tabela de decisão
    laco_   teste de laços
    custom_ parâmetros do construtor (base_limite / limite_maximo)

Cobertura estrutural (todas-arestas) e resultados: docs/relatorios/cobertura_mutacao.md.

Decisão de projeto: decidir() avalia as regras na ordem score -> limite -> valor. Um pedido
com valor inválido feito por quem tem score baixo ou não tem limite recebe o motivo da
regra anterior (score_baixo / sem_limite), e não valor_invalido.
"""

from __future__ import annotations

import pytest

from app.dominio.credito import (
    DecisorCredito,
    RegistroHistorico,
    ResultadoCredito,
    SituacaoCredito,
)

APROVADO = SituacaoCredito.APROVADO
NEGADO = SituacaoCredito.NEGADO
PARCIAL = SituacaoCredito.PARCIAL


@pytest.fixture
def decisor() -> DecisorCredito:
    """Decisor padrão: score_inicial=500, base_limite=1000, limite_maximo=50000."""
    return DecisorCredito()


@pytest.fixture
def decisor_custom() -> DecisorCredito:
    return DecisorCredito(score_inicial=600, base_limite=2000.0, limite_maximo=30000.0)


def _historico_com_score(alvo: int) -> list[RegistroHistorico]:
    """Monta um histórico que leva o score padrão (500) até ``alvo`` (0 a 1000)."""
    if alvo < 500:
        return [RegistroHistorico("consulta", peso=500 - alvo)]
    if alvo > 500:
        return [RegistroHistorico("pagamento_em_dia", peso=alvo - 500)]
    return []


class TestCalcularScore:
    # PE: uma classe por tipo de evento (7 tipos conhecidos + desconhecido), com pesos 1 e 10.
    @pytest.mark.parametrize(
        ("registros", "esperado"),
        [
            pytest.param([RegistroHistorico("pagamento_em_dia", peso=1)], 501, id="pe_pagamento_em_dia_peso1"),
            pytest.param([RegistroHistorico("pagamento_em_dia", peso=10)], 510, id="pe_pagamento_em_dia_peso10"),
            pytest.param([RegistroHistorico("atraso", peso=1)], 498, id="pe_atraso_peso1"),
            pytest.param([RegistroHistorico("atraso", peso=10)], 480, id="pe_atraso_peso10"),
            pytest.param([RegistroHistorico("negativacao", peso=1)], 495, id="pe_negativacao_peso1"),
            pytest.param([RegistroHistorico("negativacao", peso=10)], 450, id="pe_negativacao_peso10"),
            pytest.param([RegistroHistorico("consulta", peso=1)], 499, id="pe_consulta_peso1"),
            pytest.param([RegistroHistorico("consulta", peso=10)], 490, id="pe_consulta_peso10"),
            pytest.param([RegistroHistorico("cheque_sem_fundos", peso=1)], 492, id="pe_cheque_sem_fundos_peso1"),
            pytest.param([RegistroHistorico("cheque_sem_fundos", peso=5)], 460, id="pe_cheque_sem_fundos_peso5"),
            pytest.param([RegistroHistorico("contestacao_vencida", peso=1)], 497, id="pe_contestacao_vencida_peso1"),
            pytest.param([RegistroHistorico("contestacao_vencida", peso=10)], 470, id="pe_contestacao_vencida_peso10"),
            pytest.param([RegistroHistorico("adiantamento", peso=1)], 502, id="pe_adiantamento_peso1"),
            pytest.param([RegistroHistorico("adiantamento", peso=10)], 520, id="pe_adiantamento_peso10"),
            # Comportamento definido: tipo desconhecido soma +1, independentemente do peso.
            pytest.param([RegistroHistorico("tipo_desconhecido", peso=1)], 501, id="pe_tipo_desconhecido"),
            pytest.param([RegistroHistorico("tipo_desconhecido", peso=50)], 501, id="pe_tipo_desconhecido_peso_ignorado"),
            pytest.param([RegistroHistorico("pagamento_em_dia", peso=-5)], 495, id="pe_peso_negativo_inverte_sinal"),
        ],
    )
    def test_calcular_score_por_tipo_de_evento(self, decisor: DecisorCredito, registros, esperado: int):
        assert decisor.calcular_score(registros) == esperado

    # Laços: 0, 1, 2, 3 e 100 iterações sobre o histórico.
    @pytest.mark.parametrize(
        ("registros", "esperado"),
        [
            pytest.param([], 500, id="laco_0_iteracoes_score_inicial"),
            pytest.param([RegistroHistorico("pagamento_em_dia")], 501, id="laco_1_iteracao"),
            pytest.param([RegistroHistorico("pagamento_em_dia")] * 2, 502, id="laco_2_iteracoes_pagamento"),
            pytest.param([RegistroHistorico("adiantamento")] * 2, 504, id="laco_2_iteracoes_adiantamento"),
            pytest.param(
                [
                    RegistroHistorico("pagamento_em_dia", peso=5),
                    RegistroHistorico("atraso", peso=3),
                    RegistroHistorico("negativacao", peso=2),
                ],
                500 + 5 - 6 - 10,
                id="laco_3_iteracoes_tipos_mistos",
            ),
            pytest.param([RegistroHistorico("pagamento_em_dia")] * 100, 600, id="laco_100_iteracoes"),
        ],
    )
    def test_calcular_score_lacos(self, decisor: DecisorCredito, registros, esperado: int):
        assert decisor.calcular_score(registros) == esperado

    # VL: piso do score (0). "atraso" subtrai 2 x peso a partir de 500.
    @pytest.mark.parametrize(
        ("peso", "esperado"),
        [
            pytest.param(249, 2, id="vl_score_2_logo_acima_do_piso"),
            pytest.param(250, 0, id="vl_score_exatamente_0"),
            pytest.param(251, 0, id="vl_score_negativo_vira_0"),
            pytest.param(300, 0, id="vl_peso_300_clamp_0"),
            pytest.param(500, 0, id="vl_peso_muito_alto_clamp_0"),
        ],
    )
    def test_calcular_score_piso_zero(self, decisor: DecisorCredito, peso: int, esperado: int):
        assert decisor.calcular_score([RegistroHistorico("atraso", peso=peso)]) == esperado

    # VL: teto do score (1000). "adiantamento" soma 2 x peso a partir de 500.
    @pytest.mark.parametrize(
        ("peso", "esperado"),
        [
            pytest.param(200, 900, id="vl_score_900_sem_clamp"),
            pytest.param(249, 998, id="vl_score_998_logo_abaixo_do_teto"),
            pytest.param(250, 1000, id="vl_score_exatamente_1000"),
            pytest.param(251, 1000, id="vl_score_1002_vira_1000"),
            pytest.param(300, 1000, id="vl_peso_300_clamp_1000"),
        ],
    )
    def test_calcular_score_teto_mil(self, decisor: DecisorCredito, peso: int, esperado: int):
        assert decisor.calcular_score([RegistroHistorico("adiantamento", peso=peso)]) == esperado

    # VL com passo 1 (issue #47): "adiantamento" e "atraso" andam de 2 em 2 e nunca param em
    # 1001 nem em -1. "pagamento_em_dia" e "consulta" andam de 1 em 1 e testam os valores
    # exatamente vizinhos ao piso e ao teto. O caso de 1001 mata o mutante "score > 1001".
    @pytest.mark.parametrize(
        ("registro", "esperado"),
        [
            pytest.param(RegistroHistorico("pagamento_em_dia", peso=499), 999, id="vl_score_999_passo_1"),
            pytest.param(RegistroHistorico("pagamento_em_dia", peso=500), 1000, id="vl_score_1000_passo_1"),
            pytest.param(RegistroHistorico("pagamento_em_dia", peso=501), 1000, id="vl_score_1001_vira_1000"),
            pytest.param(RegistroHistorico("consulta", peso=499), 1, id="vl_score_1_passo_1"),
            pytest.param(RegistroHistorico("consulta", peso=500), 0, id="vl_score_0_passo_1"),
            pytest.param(RegistroHistorico("consulta", peso=501), 0, id="vl_score_menos_1_vira_0"),
        ],
    )
    def test_calcular_score_piso_e_teto_passo_1(self, decisor: DecisorCredito, registro, esperado: int):
        assert decisor.calcular_score([registro]) == esperado

    # Laço + VL: o clamp é aplicado a cada iteração, então a ordem dos eventos muda o resultado.
    @pytest.mark.parametrize(
        ("registros", "esperado"),
        [
            pytest.param(
                [RegistroHistorico("atraso", peso=300), RegistroHistorico("adiantamento", peso=100)],
                200,
                id="laco_clamp_no_piso_e_depois_sobe",
            ),
            pytest.param(
                [RegistroHistorico("adiantamento", peso=100), RegistroHistorico("atraso", peso=300)],
                100,
                id="laco_mesmos_eventos_em_ordem_inversa",
            ),
            pytest.param(
                [RegistroHistorico("adiantamento", peso=300), RegistroHistorico("consulta", peso=100)],
                900,
                id="laco_clamp_no_teto_e_depois_desce",
            ),
            pytest.param(
                [RegistroHistorico("consulta", peso=100), RegistroHistorico("adiantamento", peso=300)],
                1000,
                id="laco_teto_em_ordem_inversa",
            ),
        ],
    )
    def test_calcular_score_clamp_no_meio_do_laco(self, decisor: DecisorCredito, registros, esperado: int):
        assert decisor.calcular_score(registros) == esperado

    def test_calcular_score_custom_lista_vazia(self, decisor_custom: DecisorCredito):
        assert decisor_custom.calcular_score([]) == 600

    def test_calcular_score_custom_mix(self, decisor_custom: DecisorCredito):
        registros = [
            RegistroHistorico("pagamento_em_dia", peso=10),
            RegistroHistorico("adiantamento", peso=5),
        ]
        assert decisor_custom.calcular_score(registros) == 600 + 10 + 10


class TestLimitePorScore:
    # PE + VL: fronteiras das faixas de score, com renda 3000 (abaixo de todos os tetos).
    @pytest.mark.parametrize(
        ("score", "esperado"),
        [
            pytest.param(0, 0.0, id="pe_score_0_sem_limite"),
            pytest.param(100, 0.0, id="pe_score_100_sem_limite"),
            pytest.param(299, 0.0, id="vl_score_299_sem_limite"),
            pytest.param(300, 1500.0, id="vl_score_300_meia_renda"),
            pytest.param(499, 1500.0, id="vl_score_499_meia_renda"),
            pytest.param(500, 3000.0, id="vl_score_500_uma_renda"),
            pytest.param(699, 3000.0, id="vl_score_699_uma_renda"),
            pytest.param(700, 4500.0, id="vl_score_700_uma_renda_e_meia"),
            pytest.param(849, 4500.0, id="vl_score_849_uma_renda_e_meia"),
            pytest.param(850, 6000.0, id="vl_score_850_duas_rendas"),
            pytest.param(1000, 6000.0, id="vl_score_1000_duas_rendas"),
        ],
    )
    def test_limite_por_score_faixas(self, decisor: DecisorCredito, score: int, esperado: float):
        assert decisor.limite_por_score(score, 3000) == esperado

    # PE + VL: renda <= 0 não gera limite em nenhuma faixa; a menor renda positiva gera.
    @pytest.mark.parametrize(
        ("score", "renda", "esperado"),
        [
            pytest.param(500, 0, 0.0, id="vl_renda_zero"),
            pytest.param(500, -100, 0.0, id="pe_renda_negativa"),
            pytest.param(850, -1, 0.0, id="pe_renda_negativa_score_alto"),
            pytest.param(500, 0.01, 0.01, id="vl_renda_minima_positiva"),
        ],
    )
    def test_limite_por_score_renda(self, decisor: DecisorCredito, score: int, renda: float, esperado: float):
        assert decisor.limite_por_score(score, renda) == esperado

    # VL: teto de cada faixa no decisor padrão (base_limite=1000, limite_maximo=50000).
    @pytest.mark.parametrize(
        ("score", "renda", "esperado"),
        [
            # Faixa 300-499: min(renda * 0.5, base_limite * 2 = 2000)
            pytest.param(300, 3998, 1999.0, id="vl_faixa_300_abaixo_do_teto"),
            pytest.param(300, 4000, 2000.0, id="vl_faixa_300_no_teto"),
            pytest.param(499, 4002, 2000.0, id="vl_faixa_300_acima_do_teto"),
            # Faixa 500-699: min(renda * 1.0, base_limite * 10 = 10000)
            pytest.param(500, 500, 500.0, id="pe_faixa_500_renda_baixa"),
            pytest.param(500, 9999, 9999.0, id="vl_faixa_500_abaixo_do_teto"),
            pytest.param(500, 10000, 10000.0, id="vl_faixa_500_no_teto"),
            pytest.param(699, 10001, 10000.0, id="vl_faixa_500_acima_do_teto"),
            # Faixa 700-849: min(renda * 1.5, base_limite * 30 = 30000)
            pytest.param(700, 19998, 29997.0, id="vl_faixa_700_abaixo_do_teto"),
            pytest.param(700, 20000, 30000.0, id="vl_faixa_700_no_teto"),
            pytest.param(849, 20002, 30000.0, id="vl_faixa_700_acima_do_teto"),
            # Faixa 850+: min(renda * 2.0, limite_maximo = 50000)
            pytest.param(850, 24999, 49998.0, id="vl_faixa_850_abaixo_do_teto"),
            pytest.param(850, 25000, 50000.0, id="vl_faixa_850_no_teto"),
            pytest.param(1000, 25001, 50000.0, id="vl_faixa_850_acima_do_teto"),
        ],
    )
    def test_limite_por_score_tetos(self, decisor: DecisorCredito, score: int, renda: float, esperado: float):
        assert decisor.limite_por_score(score, renda) == esperado

    # Construtor: os tetos acompanham base_limite=2000 e limite_maximo=30000.
    @pytest.mark.parametrize(
        ("score", "renda", "esperado"),
        [
            pytest.param(300, 10000, 4000.0, id="custom_faixa_300_teto_base_x2"),
            pytest.param(500, 1000, 1000.0, id="custom_faixa_500_sem_teto"),
            pytest.param(500, 25000, 20000.0, id="custom_faixa_500_teto_base_x10"),
            pytest.param(850, 20000, 30000.0, id="custom_faixa_850_teto_limite_maximo"),
            pytest.param(850, 50000, 30000.0, id="custom_faixa_850_renda_muito_alta_teto_limite_maximo"),
        ],
    )
    def test_limite_por_score_custom(
        self, decisor_custom: DecisorCredito, score: int, renda: float, esperado: float
    ):
        assert decisor_custom.limite_por_score(score, renda) == esperado


class TestDecidir:
    # Tabela de decisão de decidir(). Condições, na ordem em que o código as avalia:
    #   C1 score < 300 | C2 limite == 0 | C3 valor <= 0 | C4 valor <= limite | C5 valor <= 1,5 x limite
    # Regras:
    #   R1  C1                        -> NEGADO   / score_baixo    / limite 0
    #   R2  !C1  C2                   -> NEGADO   / sem_limite     / limite 0
    #   R3  !C1 !C2  C3               -> NEGADO   / valor_invalido / limite calculado
    #   R4  !C1 !C2 !C3  C4           -> APROVADO / aprovado
    #   R5  !C1 !C2 !C3 !C4  C5       -> PARCIAL  / parcial
    #   R6  !C1 !C2 !C3 !C4 !C5       -> NEGADO   / acima_limite
    # Decisão de projeto: R1 e R2 prevalecem sobre a validação do valor (C3), por isso os
    # casos td_r1_precedencia_* e td_r2_precedencia_* têm valor inválido.
    # O resultado é comparado por inteiro (situação, score, limite e motivo).
    @pytest.mark.parametrize(
        ("score", "renda", "valor", "situacao", "limite", "motivo"),
        [
            pytest.param(0, 3000, 1000, NEGADO, 0, "score_baixo", id="td_r1_score_0"),
            pytest.param(299, 3000, 1000, NEGADO, 0, "score_baixo", id="td_r1_vl_score_299"),
            pytest.param(299, 100000, 1000, NEGADO, 0, "score_baixo", id="td_r1_score_baixo_com_renda_alta"),
            pytest.param(299, 3000, -1, NEGADO, 0, "score_baixo", id="td_r1_precedencia_sobre_valor_negativo"),
            pytest.param(500, 0, 1000, NEGADO, 0, "sem_limite", id="td_r2_vl_renda_zero"),
            pytest.param(500, -10, 1000, NEGADO, 0, "sem_limite", id="td_r2_renda_negativa"),
            pytest.param(500, 0, 0, NEGADO, 0, "sem_limite", id="td_r2_precedencia_sobre_valor_zero"),
            pytest.param(500, 3000, 0, NEGADO, 3000, "valor_invalido", id="td_r3_vl_valor_zero"),
            pytest.param(500, 3000, -1, NEGADO, 3000, "valor_invalido", id="td_r3_valor_negativo"),
            pytest.param(300, 3000, 1500, APROVADO, 1500, "aprovado", id="td_r4_vl_score_300_valor_igual_limite"),
            pytest.param(500, 3000, 0.01, APROVADO, 3000, "aprovado", id="td_r4_vl_valor_minimo"),
            pytest.param(510, 3000, 1000, APROVADO, 3000, "aprovado", id="td_r4_score_510_valor_abaixo_limite"),
            pytest.param(510, 3000, 3000, APROVADO, 3000, "aprovado", id="td_r4_vl_valor_igual_limite"),
            pytest.param(500, 3000, 3000.01, PARCIAL, 3000, "parcial", id="td_r5_vl_valor_logo_acima_do_limite"),
            pytest.param(500, 3000, 4500, PARCIAL, 3000, "parcial", id="td_r5_vl_valor_igual_1_5x_limite"),
            pytest.param(500, 3000, 4500.01, NEGADO, 3000, "acima_limite", id="td_r6_vl_valor_logo_acima_de_1_5x"),
            pytest.param(850, 3000, 10000, NEGADO, 6000, "acima_limite", id="td_r6_score_alto_valor_muito_alto"),
        ],
    )
    def test_decidir_tabela_de_decisao(
        self,
        decisor: DecisorCredito,
        score: int,
        renda: float,
        valor: float,
        situacao: SituacaoCredito,
        limite: float,
        motivo: str,
    ):
        resultado = decisor.decidir(_historico_com_score(score), renda, valor)
        assert resultado == ResultadoCredito(situacao, score, limite, motivo)

    def test_decidir_custom(self, decisor_custom: DecisorCredito):
        registros = [RegistroHistorico("pagamento_em_dia", peso=20)]
        resultado = decisor_custom.decidir(registros, 5000, 1000)
        assert resultado == ResultadoCredito(APROVADO, 620, 5000, "aprovado")
