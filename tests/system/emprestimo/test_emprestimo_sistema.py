"""Testes de sistema (Selenium) da Simulação de Empréstimo — RF05.

Automatizam os casos manuais de ``tests/testes_manuais/emprestimo/caso_emprestimo.md``
(TC-01 a TC-05), cobrindo:

- **Fluxo principal aprovado**: Price (TC-01) e SAC (TC-02).
- **Recusa por valor mínimo**: valor abaixo de R$ 100 (TC-03).
- **Recusa por prazo**: prazo=1 é bloqueado pela validação HTML5 ``min=2`` (TC-04).
- **Recusa por teto de renda**: valor acima do teto proporcional à faixa (TC-05).

Cada teste usa ``cliente_logado`` (e-mail único), garantindo independência e banco limpo.
Screenshots em caso de falha vão para ``emprestimo/falhas/``; com ``EVIDENCIAS=1`` as
etapas são registradas em ``emprestimo/evidencias/``.
"""

from __future__ import annotations

import pytest
from pagina_emprestimo import PaginaEmprestimo, RecusaEmprestimoTela, ResultadoEmprestimoTela

# ---------------------------------------------------------------------------
# TC-01 e TC-02 — Simulação aprovada (Price e SAC)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("principal", "meses", "renda", "sistema", "parcela_esperada", "total_esperado"),
    [
        pytest.param(
            1000, 12, 5000, "price", 100.46, 1205.52,
            id="tc01_price_aprovado",
        ),
        pytest.param(
            1000, 12, 5000, "sac", 113.33, 1194.96,
            id="tc02_sac_aprovado",
        ),
    ],
)
def test_simulacao_aprovada(
    navegador,
    servidor,
    cliente_logado,
    evidencia,
    principal,
    meses,
    renda,
    sistema,
    parcela_esperada,
    total_esperado,
):
    pagina = PaginaEmprestimo(navegador, servidor).abrir()
    pagina.preencher(principal, meses, renda, sistema)
    evidencia("formulario_preenchido")

    pagina.enviar()

    resultado = pagina.resultado_aprovado()
    evidencia("resultado_aprovado")

    assert resultado == ResultadoEmprestimoTela(
        aprovado=True,
        primeira_parcela=parcela_esperada,
        total=total_esperado,
        numero_parcelas=meses,
    )


# ---------------------------------------------------------------------------
# TC-03 — Recusa: valor abaixo do mínimo (R$ 100)
# ---------------------------------------------------------------------------


def test_recusa_valor_abaixo_minimo(
    navegador, servidor, cliente_logado, evidencia,
):
    pagina = PaginaEmprestimo(navegador, servidor).abrir()
    pagina.preencher(principal=50, meses=12, renda=5000, sistema="price")
    evidencia("formulario_preenchido")

    pagina.enviar()

    recusa = pagina.resultado_recusado()
    evidencia("resultado_recusado")

    assert recusa == RecusaEmprestimoTela(motivo="valor_abaixo_minimo")


# ---------------------------------------------------------------------------
# TC-04 — Prazo=1: o campo ``meses`` tem ``min=2`` no HTML, então o navegador
#         barra o envio pela validação nativa (rangeUnderflow), sem POST.
# ---------------------------------------------------------------------------


def test_prazo_abaixo_do_minimo_barrado_pelo_formulario(
    navegador, servidor, cliente_logado, evidencia,
):
    pagina = PaginaEmprestimo(navegador, servidor).abrir()
    pagina.preencher(principal=1000, meses=1, renda=5000, sistema="price")
    evidencia("formulario_preenchido")

    pagina.enviar()

    assert pagina.campo_abaixo_do_minimo("meses")
    assert not pagina.tem_resultado()
    assert navegador.current_url == servidor + PaginaEmprestimo.CAMINHO


# ---------------------------------------------------------------------------
# TC-05 — Recusa: principal acima do teto por faixa de renda.
#         renda R$ 1000 (< 2000) → teto = R$ 150. Principal R$ 200 > R$ 150.
# ---------------------------------------------------------------------------


def test_recusa_acima_teto_renda(
    navegador, servidor, cliente_logado, evidencia,
):
    pagina = PaginaEmprestimo(navegador, servidor).abrir()
    pagina.preencher(principal=200, meses=2, renda=1000, sistema="price")
    evidencia("formulario_preenchido")

    pagina.enviar()

    recusa = pagina.resultado_recusado()
    evidencia("resultado_recusado")

    assert recusa == RecusaEmprestimoTela(motivo="acima_teto")


# ---------------------------------------------------------------------------
# Teste de guarda: empréstimo exige login (redireciona para /login)
# ---------------------------------------------------------------------------


def test_emprestimo_exige_login(navegador, servidor):
    navegador.get(servidor + PaginaEmprestimo.CAMINHO)

    assert navegador.current_url == servidor + "/login"
