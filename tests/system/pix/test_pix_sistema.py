"""Testes de sistema (Selenium) da Transferência PIX — RF03.

Automatizam os casos manuais de ``tests/testes_manuais/pix/caso_pix.md`` (TC-01 a TC-04),
cobrindo:

- **Fluxo principal aprovado**: CPF válido com saldo suficiente (TC-01).
- **Recusa por chave inválida**: CPF inválido (TC-02).
- **Recusa por saldo insuficiente** (TC-03).
- **Regressão do defeito #16**: e-mail com dois ``@`` recusado (TC-04).
- **Valor 0 barrado pela validação HTML5** ``min="0.01"`` (TC-05).
- **Guarda de autenticação**: ``/pix`` sem login redireciona para ``/login``.

Determinismo: os cenários usam valores válidos tanto na janela diurna quanto na noturna
(limite noturno R$ 1.000,00), para não depender do relógio da máquina. O saldo inicial é
definido direto no SQLite temporário pela fixture ``definir_saldo_sistema`` (a interface
não tem depósito). Cada teste usa ``cliente_logado`` (e-mail único), garantindo independência.
Screenshots em caso de falha vão para ``pix/falhas/``; com ``EVIDENCIAS=1`` as etapas são
registradas em ``pix/evidencias/``.
"""

from __future__ import annotations

from pagina_pix import PaginaPix

CPF_VALIDO = "529.982.247-25"
CPF_INVALIDO = "123.456.789-00"


def test_pix_aprovado_com_cpf(
    navegador, servidor, cliente_logado, definir_saldo_sistema, evidencia,
):
    definir_saldo_sistema(cliente_logado, 1000.0)
    pagina = PaginaPix(navegador, servidor).abrir()
    pagina.preencher(chave=CPF_VALIDO, tipo="cpf", valor="100.00")
    evidencia("formulario_preenchido")

    pagina.enviar()

    assert pagina.mensagem_flash() == "Transferência realizada com sucesso."
    assert navegador.current_url == servidor + "/"
    saldo, extrato = pagina.dados_dashboard()
    evidencia("dashboard_apos_pix")

    assert saldo == 900.0
    assert any("PIX cpf" in linha and "-100.00" in linha for linha in extrato)


def test_pix_recusado_por_chave_invalida(
    navegador, servidor, cliente_logado, definir_saldo_sistema, evidencia,
):
    definir_saldo_sistema(cliente_logado, 1000.0)
    pagina = PaginaPix(navegador, servidor).abrir()
    pagina.preencher(chave=CPF_INVALIDO, tipo="cpf", valor="50.00")
    evidencia("formulario_preenchido")

    pagina.enviar()

    assert pagina.mensagem_flash() == "Chave PIX inválida."
    assert navegador.current_url == servidor + PaginaPix.CAMINHO
    saldo, extrato = pagina.dados_dashboard()
    evidencia("dashboard_saldo_intacto")

    assert saldo == 1000.0
    assert extrato == []


def test_pix_recusado_por_saldo_insuficiente(
    navegador, servidor, cliente_logado, definir_saldo_sistema, evidencia,
):
    definir_saldo_sistema(cliente_logado, 100.0)
    pagina = PaginaPix(navegador, servidor).abrir()
    pagina.preencher(chave=CPF_VALIDO, tipo="cpf", valor="500.00")
    evidencia("formulario_preenchido")

    pagina.enviar()

    assert pagina.mensagem_flash() == "Saldo insuficiente."
    assert navegador.current_url == servidor + PaginaPix.CAMINHO
    saldo, extrato = pagina.dados_dashboard()
    evidencia("dashboard_saldo_intacto")

    assert saldo == 100.0
    assert extrato == []


def test_pix_recusado_email_com_dois_arrobas_regressao_16(
    navegador, servidor, cliente_logado, definir_saldo_sistema, evidencia,
):
    """Regressão do defeito #16: e-mail com dois '@' é recusado como chave inválida."""
    definir_saldo_sistema(cliente_logado, 1000.0)
    pagina = PaginaPix(navegador, servidor).abrir()
    pagina.preencher(chave="a@b@c.com", tipo="email", valor="25.00")
    evidencia("formulario_preenchido")

    pagina.enviar()

    assert pagina.mensagem_flash() == "Chave PIX inválida."
    assert navegador.current_url == servidor + PaginaPix.CAMINHO
    saldo, extrato = pagina.dados_dashboard()
    evidencia("dashboard_saldo_intacto")

    assert saldo == 1000.0
    assert extrato == []


def test_pix_valor_zero_barrado_pelo_formulario(
    navegador, servidor, cliente_logado, definir_saldo_sistema, evidencia,
):
    definir_saldo_sistema(cliente_logado, 1000.0)
    pagina = PaginaPix(navegador, servidor).abrir()
    pagina.preencher(chave=CPF_VALIDO, tipo="cpf", valor="0")
    evidencia("formulario_preenchido")

    pagina.enviar()

    assert pagina.campo_abaixo_do_minimo("valor")
    assert not pagina.tem_flash()
    assert navegador.current_url == servidor + PaginaPix.CAMINHO


def test_pix_exige_login(navegador, servidor):
    navegador.get(servidor + PaginaPix.CAMINHO)

    assert navegador.current_url == servidor + "/login"
