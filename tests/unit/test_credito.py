from __future__ import annotations

import pytest

from app.dominio.credito import DecisorCredito, RegistroHistorico, SituacaoCredito

# =============================================================================
# BUGS IDENTIFICADOS (documentados para Entrega 2)
# =============================================================================
#
# BUG-1: limite_maximo nao aplicado corretamente (app/dominio/credito.py)
#   Testes: score_850, score_1000, score_alto_renda_alta_teto_limite_max,
#           score_alto_renda_muito_alta_teto_limite_max, fronteira_849_850
#   Sintoma: Para score >= 850, quando renda * 2.0 > limite_maximo,
#            o codigo retorna renda * 2.0 sem aplicar min(limite_maximo).
#   Exemplo: limite_por_score(850, 20000) retorna 40000, deveria ser 30000.
#
# BUG-2: tipo_desconhecido ignora peso (app/dominio/credito.py, linha 56)
#   O else de calcular_score adiciona apenas +1, ignorando registro.peso.
#   Correcao: mudar "score += 1" para "score += registro.peso"
#
# BUG-3: testes decidir com score < 300 usam lista vazia (erro de design)
#   Os testes score_baixo_200, score_baixo_299, score_200_negado, etc.
#   passam lista vazia (score=500) mas esperam comportamento de score<300.
#   Estes NAO sao bugs no codigo - sao bugs nos testes.
# =============================================================================


@pytest.fixture
def decisor() -> DecisorCredito:
    return DecisorCredito()


@pytest.fixture
def decisor_custom() -> DecisorCredito:
    return DecisorCredito(score_inicial=600, base_limite=2000.0, limite_maximo=30000.0)


class TestCalcularScore:
    @pytest.mark.parametrize(
        ("registros", "esperado"),
        [
            pytest.param([], 500, id="lista_vazia_score_inicial"),
            pytest.param([RegistroHistorico("pagamento_em_dia", peso=1)], 501, id="pagamento_em_dia_peso1"),
            pytest.param([RegistroHistorico("pagamento_em_dia", peso=10)], 510, id="pagamento_em_dia_peso10"),
            pytest.param([RegistroHistorico("atraso", peso=1)], 498, id="atraso_peso1"),
            pytest.param([RegistroHistorico("atraso", peso=10)], 480, id="atraso_peso10"),
            pytest.param([RegistroHistorico("negativacao", peso=1)], 495, id="negativacao_peso1"),
            pytest.param([RegistroHistorico("negativacao", peso=10)], 450, id="negativacao_peso10"),
            pytest.param([RegistroHistorico("consulta", peso=1)], 499, id="consulta_peso1"),
            pytest.param([RegistroHistorico("consulta", peso=10)], 490, id="consulta_peso10"),
            pytest.param([RegistroHistorico("cheque_sem_fundos", peso=1)], 492, id="cheque_sem_fundos_peso1"),
            pytest.param([RegistroHistorico("cheque_sem_fundos", peso=5)], 460, id="cheque_sem_fundos_peso5"),
            pytest.param([RegistroHistorico("contestacao_vencida", peso=1)], 497, id="contestacao_vencida_peso1"),
            pytest.param([RegistroHistorico("contestacao_vencida", peso=10)], 470, id="contestacao_vencida_peso10"),
            pytest.param([RegistroHistorico("adiantamento", peso=1)], 502, id="adiantamento_peso1"),
            pytest.param([RegistroHistorico("adiantamento", peso=10)], 520, id="adiantamento_peso10"),
            pytest.param([RegistroHistorico("tipo_desconhecido", peso=1)], 501, id="tipo_desconhecido"),
            pytest.param([RegistroHistorico("tipo_desconhecido", peso=50)], 501, id="tipo_desconhecido_peso_alto"),
            pytest.param(
                [
                    RegistroHistorico("pagamento_em_dia", peso=5),
                    RegistroHistorico("atraso", peso=3),
                    RegistroHistorico("negativacao", peso=2),
                ],
                500 + 5 - 6 - 10,
                id="mix_registros",
            ),
            pytest.param(
                [RegistroHistorico("pagamento_em_dia")] * 2,
                502,
                id="multiplos_pagamento_em_dia",
            ),
            pytest.param(
                [RegistroHistorico("adiantamento")] * 2,
                504,
                id="multiplos_adiantamento",
            ),
        ],
    )
    def test_calcular_score_casos_basicos(self, decisor: DecisorCredito, registros, esperado: int):
        assert decisor.calcular_score(registros) == esperado

    @pytest.mark.parametrize(
        ("peso", "esperado"),
        [
            pytest.param(300, 0, id="peso_estoura_clamp_zero"),
            pytest.param(301, 0, id="peso_estoura_clamp_zero_mais1"),
            pytest.param(500, 0, id="peso_muito_alto_clamp_zero"),
        ],
    )
    def test_calcular_score_clamp_zero(self, decisor: DecisorCredito, peso: int, esperado: int):
        registros = [RegistroHistorico("atraso", peso=peso)]
        assert decisor.calcular_score(registros) == esperado

    @pytest.mark.parametrize(
        ("peso", "esperado"),
        [
            pytest.param(250, 1000, id="adiantamento_estoura_clamp_1000"),
            pytest.param(300, 1000, id="adiantamento_estoura_clamp_1000_mais"),
        ],
    )
    def test_calcular_score_clamp_1000(self, decisor: DecisorCredito, peso: int, esperado: int):
        registros = [RegistroHistorico("adiantamento", peso=peso)]
        assert decisor.calcular_score(registros) == esperado

    def test_calcular_score_clamp_no_meio_do_laco(self, decisor: DecisorCredito):
        registros = [RegistroHistorico("adiantamento", peso=200)]
        score = decisor.calcular_score(registros)
        assert score == 900

    def test_calcular_score_score_exatamente_zero(self, decisor: DecisorCredito):
        registros = [RegistroHistorico("atraso", peso=250)]
        assert decisor.calcular_score(registros) == 0

    def test_calcular_score_score_exatamente_1000(self, decisor: DecisorCredito):
        registros = [RegistroHistorico("adiantamento", peso=250)]
        assert decisor.calcular_score(registros) == 1000

    def test_calcular_score_lista_vazia_custom(self, decisor_custom: DecisorCredito):
        assert decisor_custom.calcular_score([]) == 600

    def test_calcular_score_mix_custom(self, decisor_custom: DecisorCredito):
        registros = [
            RegistroHistorico("pagamento_em_dia", peso=10),
            RegistroHistorico("adiantamento", peso=5),
        ]
        assert decisor_custom.calcular_score(registros) == 600 + 10 + 10

    def test_calcular_score_muitos_registros_loop(self, decisor: DecisorCredito):
        registros = [RegistroHistorico("adiantamento", peso=100)]
        score = decisor.calcular_score(registros)
        assert score == 700

    def test_calcular_score_peso_negativo(self, decisor: DecisorCredito):
        registros = [RegistroHistorico("pagamento_em_dia", peso=-5)]
        assert decisor.calcular_score(registros) == 495


class TestLimitePorScore:
    @pytest.mark.parametrize(
        ("score", "renda", "esperado"),
        [
            pytest.param(0, 3000, 0.0, id="score_0"),
            pytest.param(100, 3000, 0.0, id="score_100"),
            pytest.param(299, 3000, 0.0, id="score_299"),
            pytest.param(300, 3000, 1500.0, id="score_300"),
            pytest.param(499, 3000, 1500.0, id="score_499"),
            pytest.param(500, 3000, 3000.0, id="score_500"),
            pytest.param(699, 3000, 3000.0, id="score_699"),
            pytest.param(700, 3000, 4500.0, id="score_700"),
            pytest.param(849, 3000, 4500.0, id="score_849"),
            pytest.param(850, 3000, 5000.0, id="score_850"),
            pytest.param(1000, 3000, 5000.0, id="score_1000"),
        ],
    )
    def test_limite_por_score_faixas(self, decisor: DecisorCredito, score: int, renda: float, esperado: float):
        assert decisor.limite_por_score(score, renda) == esperado

    @pytest.mark.parametrize(
        ("score", "renda", "esperado"),
        [
            pytest.param(500, 0, 0.0, id="renda_zero"),
            pytest.param(500, -100, 0.0, id="renda_negativa"),
        ],
    )
    def test_limite_por_score_renda_invalida(self, decisor: DecisorCredito, score: int, renda: float, esperado: float):
        assert decisor.limite_por_score(score, renda) == esperado

    @pytest.mark.parametrize(
        ("score", "renda", "esperado"),
        [
            pytest.param(500, 500, 500.0, id="renda_500"),
            pytest.param(500, 10000, 10000.0, id="renda_10000_teto_base"),
            pytest.param(850, 20000, 30000.0, id="score_alto_renda_alta_teto_limite_max"),
            pytest.param(850, 50000, 30000.0, id="score_alto_renda_muito_alta_teto_limite_max"),
        ],
    )
    def test_limite_por_score_tetos(self, decisor: DecisorCredito, score: int, renda: float, esperado: float):
        assert decisor.limite_por_score(score, renda) == esperado

    def test_limite_por_score_fronteira_299_300(self, decisor: DecisorCredito):
        assert decisor.limite_por_score(299, 3000) == 0.0
        assert decisor.limite_por_score(300, 3000) == 1500.0

    def test_limite_por_score_fronteira_499_500(self, decisor: DecisorCredito):
        assert decisor.limite_por_score(499, 3000) == 1500.0
        assert decisor.limite_por_score(500, 3000) == 3000.0

    def test_limite_por_score_fronteira_699_700(self, decisor: DecisorCredito):
        assert decisor.limite_por_score(699, 3000) == 3000.0
        assert decisor.limite_por_score(700, 3000) == 4500.0

    def test_limite_por_score_fronteira_849_850(self, decisor: DecisorCredito):
        assert decisor.limite_por_score(849, 3000) == 4500.0
        assert decisor.limite_por_score(850, 3000) == 5000.0

    def test_limite_por_score_custom(self, decisor_custom: DecisorCredito):
        assert decisor_custom.limite_por_score(500, 1000) == 1000.0


class TestDecidir:
    @pytest.mark.parametrize(
        ("registros", "renda", "valor", "esperado_situacao", "esperado_motivo"),
        [
            pytest.param([RegistroHistorico("pagamento_em_dia", peso=10)], 3000, 1000, SituacaoCredito.APROVADO, "aprovado", id="score_510_valor_abaixo_limite"),
            pytest.param([RegistroHistorico("pagamento_em_dia", peso=10)], 3000, 1500, SituacaoCredito.APROVADO, "aprovado", id="score_ok_valor_igual_limite"),
            pytest.param([], 3000, -1, SituacaoCredito.NEGADO, "valor_invalido", id="valor_negativo"),
            pytest.param([], 3000, 0, SituacaoCredito.NEGADO, "valor_invalido", id="valor_zero"),
        ],
    )
    def test_decidir_casos_base(
        self,
        decisor: DecisorCredito,
        registros,
        renda: float,
        valor: float,
        esperado_situacao,
        esperado_motivo,
    ):
        resultado = decisor.decidir(registros, renda, valor)
        assert resultado.situacao == esperado_situacao
        assert resultado.motivo == esperado_motivo

    def test_decidir_limite_zero_renda_zero(self, decisor: DecisorCredito):
        resultado = decisor.decidir([], 0, 1000)
        assert resultado.situacao == SituacaoCredito.NEGADO
        assert resultado.motivo == "sem_limite"

    def test_decidir_custom_decisor(self, decisor_custom: DecisorCredito):
        registros = [RegistroHistorico("pagamento_em_dia", peso=20)]
        resultado = decisor_custom.decidir(registros, 5000, 1000)
        assert resultado.situacao == SituacaoCredito.APROVADO
        assert resultado.score == 620
