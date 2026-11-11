"""Fixtures compartilhadas dos testes de sistema (Selenium).

Organização: uma pasta por funcionalidade (ex.: ``tests/system/credito/``), com o arquivo de
testes ``test_<funcionalidade>_sistema.py``, o page object ``pagina_<funcionalidade>.py`` e as
evidências. Estas fixtures valem para todas as pastas.

- ``servidor``: sobe a aplicação Flask real numa thread, em porta livre, com um banco SQLite
  temporário (criado do zero a cada execução da suíte).
- ``navegador``: Chrome headless, com o driver resolvido pelo Selenium Manager. A instância é
  reaproveitada na sessão, mas os cookies são apagados antes de cada teste.
- ``cliente_logado``: cadastra um cliente novo (e-mail único) pela tela ``/registro``, que já
  deixa a sessão aberta. Cada teste usa o seu próprio cliente, então os testes são independentes.

- ``evidencia``: função para registrar o screenshot de uma etapa do teste, ex.:
  ``evidencia("formulario_preenchido")``. Só grava com ``EVIDENCIAS=1``.

Evidências, sempre dentro da pasta da funcionalidade:
- em caso de falha, screenshot e HTML vão para ``<funcionalidade>/falhas/`` (fora do git);
- com ``EVIDENCIAS=1``, as etapas registradas e a tela final de cada teste vão para
  ``<funcionalidade>/evidencias/``, numeradas na ordem (``<teste>__1_<etapa>.png``,
  ``<teste>__2_final.png``...).
"""

from __future__ import annotations

import os
import re
import threading
import uuid
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from werkzeug.serving import make_server

from app import create_app
from app.config import Config

SENHA_PADRAO = "senha123"
ESPERA_SEGUNDOS = 5


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda o relatório de cada fase no item, para a fixture saber se o teste falhou."""
    resultado = yield
    relatorio = resultado.get_result()
    setattr(item, f"relatorio_{relatorio.when}", relatorio)


def _evidencias_ligadas() -> bool:
    return os.environ.get("EVIDENCIAS") == "1"


def _nome_do_teste(item) -> str:
    return re.sub(r"[^\w.-]+", "_", item.name).strip("_")


def _salvar_evidencia(driver, item, etapa: str) -> None:
    """Salva o screenshot de uma etapa, numerado na ordem em que as etapas acontecem."""
    item.evidencias_salvas = getattr(item, "evidencias_salvas", 0) + 1
    pasta = Path(item.path).parent / "evidencias"
    pasta.mkdir(exist_ok=True)
    arquivo = f"{_nome_do_teste(item)}__{item.evidencias_salvas}_{etapa}.png"
    driver.save_screenshot(str(pasta / arquivo))


@pytest.fixture(scope="session")
def servidor(tmp_path_factory) -> str:
    banco = tmp_path_factory.mktemp("sistema") / "banco_sistema.db"

    class ConfigSistema(Config):
        TESTING = True
        DATABASE = str(banco)
        SECRET_KEY = "chave-dos-testes-de-sistema"

    servidor_http = make_server("127.0.0.1", 0, create_app(ConfigSistema), threaded=True)
    thread = threading.Thread(target=servidor_http.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{servidor_http.server_port}"
    servidor_http.shutdown()
    thread.join(timeout=5)


@pytest.fixture(scope="session")
def _navegador_da_sessao():
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1280,900")
    # Idioma fixo: os campos type="number" passam a aceitar "." como separador decimal.
    opcoes.add_argument("--lang=en-US")
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    try:
        driver = webdriver.Chrome(options=opcoes)
    except WebDriverException as erro:
        pytest.skip(f"Chrome/ChromeDriver indisponível para os testes de sistema: {erro.msg}")
    yield driver
    driver.quit()


@pytest.fixture
def navegador(_navegador_da_sessao, servidor, request):
    driver = _navegador_da_sessao
    driver.get(servidor + "/login")
    driver.delete_all_cookies()
    yield driver
    relatorio = getattr(request.node, "relatorio_call", None)
    if relatorio is not None and relatorio.failed:
        nome = _nome_do_teste(request.node)
        pasta = Path(request.node.path).parent / "falhas"
        pasta.mkdir(exist_ok=True)
        driver.save_screenshot(str(pasta / f"{nome}.png"))
        (pasta / f"{nome}.html").write_text(driver.page_source, encoding="utf-8")
    elif _evidencias_ligadas():
        _salvar_evidencia(driver, request.node, "final")


@pytest.fixture
def evidencia(navegador, request):
    """Retorna uma função que registra o screenshot de uma etapa (só com EVIDENCIAS=1)."""

    def registrar(etapa: str) -> None:
        if _evidencias_ligadas():
            _salvar_evidencia(navegador, request.node, etapa)

    return registrar


@pytest.fixture
def cliente_logado(navegador, servidor) -> str:
    """Cadastra um cliente com e-mail único pela interface; retorna o e-mail."""
    email = f"cliente-{uuid.uuid4().hex[:10]}@teste.com"
    navegador.get(servidor + "/registro")
    navegador.find_element(By.NAME, "nome").send_keys("Cliente Teste")
    navegador.find_element(By.NAME, "email").send_keys(email)
    navegador.find_element(By.NAME, "senha").send_keys(SENHA_PADRAO)
    navegador.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    WebDriverWait(navegador, ESPERA_SEGUNDOS).until(EC.url_to_be(servidor + "/"))
    return email
