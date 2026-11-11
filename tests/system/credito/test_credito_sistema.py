"""Testes de sistema (Selenium) da Análise de Crédito — RF06, issue #60.

Automatizam os casos manuais de ``tests/testes_manuais/credito/caso_credito.md`` (CT-01 a CT-10),
com o mesmo id, e acrescentam duas fronteiras (CT-11 e CT-12).

A tela ``/credito`` chama ``DecisorCredito().decidir([], renda, valor)``: sem histórico, o score é
sempre 500, e o limite fica em ``min(renda, 10000)``.
"""

from __future__ import annotations

import pytest
from pagina_credito import PaginaCredito, ResultadoCreditoTela

SCORE_SEM_HISTORICO = 500


@pytest.mark.parametrize(
    ("renda", "valor", "situacao", "limite", "motivo"),
    [
        pytest.param(10000, 5000, "aprovado", 10000.0, "aprovado", id="ct01_aprovado_dentro_do_limite"),
        pytest.param(10000, 10000, "aprovado", 10000.0, "aprovado", id="ct02_aprovado_exatamente_no_limite"),
        pytest.param(10000, 12000, "parcial", 10000.0, "parcial", id="ct03_parcial_entre_limite_e_1_5x"),
        pytest.param(10000, 20000, "negado", 10000.0, "acima_limite", id="ct04_negado_acima_de_1_5x"),
        pytest.param(10000, 0, "negado", 10000.0, "valor_invalido", id="ct05_negado_valor_zero"),
        pytest.param(0, 5000, "negado", 0.0, "sem_limite", id="ct07_negado_renda_zero"),
        pytest.param(10000, 15000, "parcial", 10000.0, "parcial", id="ct09_parcial_exatamente_1_5x"),
        pytest.param(10000, "14999.99", "parcial", 10000.0, "parcial", id="ct10_parcial_logo_abaixo_de_1_5x"),
        pytest.param(10000, "15000.01", "negado", 10000.0, "acima_limite", id="ct11_negado_logo_acima_de_1_5x"),
        pytest.param(20000, 10000, "aprovado", 10000.0, "aprovado", id="ct12_limite_no_teto_da_faixa"),
    ],
)
def test_analise_de_credito(navegador, servidor, cliente_logado, renda, valor, situacao, limite, motivo):
    pagina = PaginaCredito(navegador, servidor).abrir()

    pagina.analisar(renda, valor)

    assert pagina.resultado() == ResultadoCreditoTela(situacao, SCORE_SEM_HISTORICO, limite, motivo)


@pytest.mark.parametrize(
    ("campo", "renda", "valor"),
    [
        pytest.param("valor", 10000, -500, id="ct06_valor_negativo_bloqueado"),
        pytest.param("renda", -1000, 5000, id="ct08_renda_negativa_bloqueada"),
    ],
)
def test_valor_negativo_e_barrado_pelo_formulario(navegador, servidor, cliente_logado, campo, renda, valor):
    pagina = PaginaCredito(navegador, servidor).abrir()

    pagina.analisar(renda, valor)

    assert pagina.campo_abaixo_do_minimo(campo)
    assert not pagina.tem_resultado()
    assert navegador.current_url == servidor + PaginaCredito.CAMINHO


def test_credito_exige_login(navegador, servidor):
    navegador.get(servidor + PaginaCredito.CAMINHO)

    assert navegador.current_url == servidor + "/login"
