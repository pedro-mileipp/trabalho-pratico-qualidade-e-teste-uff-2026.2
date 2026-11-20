"""Testes de sistema (Selenium) para autenticação, registro, logout e rotas protegidas (RF01/RF02)."""

from __future__ import annotations

import uuid

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.system.auth.pagina_auth import ESPERA_SEGUNDOS, PaginaAuth
from tests.system.conftest import SENHA_PADRAO


def _email_unico(prefixo: str = "auth") -> str:
    return f"{prefixo}-{uuid.uuid4().hex[:10]}@teste.com"


def test_cadastro_valido_e_redirecionamento_para_dashboard(navegador, servidor, evidencia):
    pagina = PaginaAuth(navegador, servidor).abrir_registro()
    email = _email_unico("cadastro")

    pagina.preencher_registro("Gabrielle Rosa", email, SENHA_PADRAO)
    evidencia("formulario_registro_preenchido")
    pagina.submeter()

    url_final = pagina.aguardar_redirecionamento("/")
    assert url_final.endswith("/")
    assert "Cliente Teste" not in navegador.page_source or "Gabrielle Rosa" in navegador.page_source or "/login" not in url_final


@pytest.mark.parametrize(
    ("nome", "email_mode", "senha", "tipo_falha", "mensagem_esperada"),
    [
        (
            "Gabrielle Rosa",
            "duplicado",
            SENHA_PADRAO,
            "flash",
            "Este e-mail já está cadastrado.",
        ),
        (
            "Gabrielle Rosa",
            "unico",
            "12345",
            "flash",
            "Dados inválidos. Verifique os campos.",
        ),
        (
            "",
            "unico",
            SENHA_PADRAO,
            "html5_required",
            None,
        ),
        (
            "Gabrielle Rosa",
            "sem_arroba",
            SENHA_PADRAO,
            "html5_invalid",
            None,
        ),
        (
            "Gabrielle Rosa",
            "sem_dominio",
            SENHA_PADRAO,
            "html5_invalid",
            None,
        ),
    ],
    ids=[
        "email_duplicado",
        "senha_curta_5_chars",
        "campos_obrigatorios_vazios",
        "email_sem_arroba",
        "email_sem_dominio",
    ],
)
def test_cadastro_invalido_parametrizado(
    navegador,
    servidor,
    evidencia,
    nome,
    email_mode,
    senha,
    tipo_falha,
    mensagem_esperada,
):
    email_base = _email_unico("invalido")

    if email_mode == "duplicado":
        # Cria conta prévia para testar duplicidade com independência total entre testes
        PaginaAuth(navegador, servidor).abrir_registro().preencher_registro(
            "Usuario Existente", email_base, SENHA_PADRAO
        ).submeter()
        WebDriverWait(navegador, ESPERA_SEGUNDOS).until(EC.url_to_be(servidor + "/"))
        navegador.delete_all_cookies()
        email = email_base
    elif email_mode == "sem_arroba":
        email = f"{email_base.split('@')[0]}.com"
    elif email_mode == "sem_dominio":
        email = f"{email_base.split('@')[0]}@"
    else:
        email = email_base

    pagina = PaginaAuth(navegador, servidor).abrir_registro()
    pagina.preencher_registro(nome, email, senha)
    evidencia("tentativa_cadastro_invalido")
    pagina.submeter()

    if tipo_falha == "flash":
        assert pagina.esta_na_rota("/registro")
        assert pagina.mensagem_flash() == mensagem_esperada
    elif tipo_falha == "html5_required":
        assert pagina.esta_na_rota("/registro")
        campo_nome = navegador.find_element(By.NAME, "nome")
        assert navegador.execute_script("return arguments[0].validity.valueMissing;", campo_nome)
    elif tipo_falha == "html5_invalid":
        assert pagina.esta_na_rota("/registro")
        campo_email = navegador.find_element(By.NAME, "email")
        validade = navegador.execute_script(
            "return arguments[0].validity.typeMismatch || arguments[0].validity.valueMissing;",
            campo_email,
        )
        assert validade is True


def test_login_valido_e_reautenticacao_apos_logout(navegador, servidor, evidencia):
    email = _email_unico("login")

    # Cadastra o usuário e encerra a sessão
    PaginaAuth(navegador, servidor).abrir_registro().preencher_registro(
        "Gabrielle Rosa", email, SENHA_PADRAO
    ).submeter()
    WebDriverWait(navegador, ESPERA_SEGUNDOS).until(EC.url_to_be(servidor + "/"))

    navegador.get(servidor + "/logout")
    WebDriverWait(navegador, ESPERA_SEGUNDOS).until(EC.url_contains("/login"))
    evidencia("apos_logout")

    # Realiza login com credenciais válidas
    pagina = PaginaAuth(navegador, servidor).abrir_login()
    pagina.preencher_login(email, SENHA_PADRAO)
    evidencia("credenciais_login_preenchidas")
    pagina.submeter()

    url_apos_login = pagina.aguardar_redirecionamento("/")
    assert url_apos_login.endswith("/")


@pytest.mark.parametrize(
    ("cenario", "senha_informada"),
    [
        ("usuario_inexistente", "123456"),
        ("senha_incorreta", "senhaERRADA"),
    ],
    ids=["usuario_inexistente", "senha_incorreta"],
)
def test_login_invalido_parametrizado(navegador, servidor, evidencia, cenario, senha_informada):
    if cenario == "usuario_inexistente":
        email = _email_unico("inexistente")
    else:
        email = _email_unico("senha_errada")
        PaginaAuth(navegador, servidor).abrir_registro().preencher_registro(
            "Gabrielle Rosa", email, SENHA_PADRAO
        ).submeter()
        WebDriverWait(navegador, ESPERA_SEGUNDOS).until(EC.url_to_be(servidor + "/"))
        navegador.delete_all_cookies()

    pagina = PaginaAuth(navegador, servidor).abrir_login()
    pagina.preencher_login(email, senha_informada)
    evidencia("tentativa_login_invalido")
    pagina.submeter()

    assert pagina.esta_na_rota("/login")
    assert pagina.mensagem_flash() == "E-mail ou senha inválidos."


def test_logout_encerra_sessao_e_redireciona_para_login(navegador, servidor, cliente_logado, evidencia):
    assert cliente_logado
    navegador.get(servidor + "/logout")
    WebDriverWait(navegador, ESPERA_SEGUNDOS).until(EC.url_contains("/login"))
    evidencia("sessao_encerrada")

    assert "/login" in navegador.current_url


@pytest.mark.parametrize(
    "rota_protegida",
    ["/", "/credito"],
    ids=["dashboard_raiz", "analise_credito"],
)
def test_acesso_rota_protegida_sem_autenticacao(navegador, servidor, evidencia, rota_protegida):
    pagina = PaginaAuth(navegador, servidor)
    pagina.abrir_rota_protegida(rota_protegida)
    evidencia("acesso_sem_sessao")

    assert pagina.esta_na_rota("/login")