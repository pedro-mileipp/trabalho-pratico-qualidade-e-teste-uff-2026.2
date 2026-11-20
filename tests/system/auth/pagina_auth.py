"""Page object das telas de autenticação (``/login`` e ``/registro``) e navegação protegida."""

from __future__ import annotations

from urllib.parse import urljoin

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ESPERA_SEGUNDOS = 5


class PaginaAuth:
    CAMINHO_LOGIN = "/login"
    CAMINHO_REGISTRO = "/registro"

    CAMPO_NOME = (By.NAME, "nome")
    CAMPO_EMAIL = (By.NAME, "email")
    CAMPO_SENHA = (By.NAME, "senha")
    BOTAO_SUBMIT = (By.CSS_SELECTOR, "form button[type='submit']")
    LINK_REGISTRO = (By.CSS_SELECTOR, "form ~ p a[href*='/registro'], p a[href*='/registro']")
    LINK_LOGIN = (By.CSS_SELECTOR, "form ~ p a[href*='/login'], p a[href*='/login']")
    MENSAGENS_FLASH = (By.CSS_SELECTOR, ".flash, .alert, .erro, [role='alert'], .cartao p")

    def __init__(self, navegador: WebDriver, servidor: str) -> None:
        self._navegador = navegador
        self._servidor = servidor.rstrip("/")

    def _url(self, caminho: str) -> str:
        if caminho.startswith(("http://", "https://")):
            return caminho
        caminho_normalizado = caminho if caminho.startswith("/") else f"/{caminho}"
        return urljoin(f"{self._servidor}/", caminho_normalizado.lstrip("/"))

    def abrir_login(self) -> PaginaAuth:
        self._navegador.get(self._url(self.CAMINHO_LOGIN))
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.CAMPO_EMAIL)
        )
        return self

    def abrir_registro(self) -> PaginaAuth:
        self._navegador.get(self._url(self.CAMINHO_REGISTRO))
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.CAMPO_NOME)
        )
        return self

    def abrir_rota_protegida(self, caminho: str, aguardar_seletor: tuple[str, str] | None = None) -> PaginaAuth:
        """Abre uma rota protegida (ex.: ``/`` ou ``/credito``) e aguarda estabilizar URL ou elemento."""
        url_destino = self._url(caminho)
        self._navegador.get(url_destino)
        if aguardar_seletor is not None:
            WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
                EC.presence_of_element_located(aguardar_seletor)
            )
        else:
            WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
                lambda drv: drv.current_url != "about:blank"
            )
        return self

    def preencher_login(self, email: str, senha: str) -> PaginaAuth:
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.CAMPO_EMAIL)
        )
        self._preencher(self.CAMPO_EMAIL, email)
        self._preencher(self.CAMPO_SENHA, senha)
        return self

    def preencher_registro(self, nome: str, email: str, senha: str) -> PaginaAuth:
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.CAMPO_NOME)
        )
        self._preencher(self.CAMPO_NOME, nome)
        self._preencher(self.CAMPO_EMAIL, email)
        self._preencher(self.CAMPO_SENHA, senha)
        return self

    def submeter(self) -> PaginaAuth:
        botao = WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.element_to_be_clickable(self.BOTAO_SUBMIT)
        )
        botao.click()
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            lambda drv: drv.execute_script("return document.readyState") == "complete"
        )
        return self

    def ir_para_registro(self) -> PaginaAuth:
        link = WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.element_to_be_clickable(self.LINK_REGISTRO)
        )
        link.click()
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.CAMPO_NOME)
        )
        return self

    def ir_para_login(self) -> PaginaAuth:
        link = WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.element_to_be_clickable(self.LINK_LOGIN)
        )
        link.click()
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.CAMPO_EMAIL)
        )
        return self

    def mensagens(self) -> list[str]:
        """Retorna mensagens exibidas na tela (ex.: flash de erro em ``app/web/routes/auth.py``)."""
        elementos = self._navegador.find_elements(*self.MENSAGENS_FLASH)
        textos: list[str] = []
        for elem in elementos:
            try:
                texto = elem.text.strip()
            except StaleElementReferenceException:
                continue
            if not texto:
                continue
            # Evita capturar o parágrafo auxiliar com link de alternância ("Não tem conta? ...")
            if texto.startswith(("Não tem conta?", "Já tem conta?")):
                continue
            if texto not in textos:
                textos.append(texto)
        return textos

    def mensagem_flash(self, timeout: float = ESPERA_SEGUNDOS) -> str | None:
        """Aguarda e retorna a primeira mensagem relevante encontrada ou ``None``."""
        try:
            WebDriverWait(self._navegador, timeout).until(lambda _drv: bool(self.mensagens()))
        except TimeoutException:
            return None
        mensagens = self.mensagens()
        return mensagens[0] if mensagens else None

    def aguardar_redirecionamento(self, caminho_ou_url: str, timeout: float = ESPERA_SEGUNDOS) -> str:
        """Aguarda a URL atingir o destino esperado e retorna ``current_url``."""
        url_esperada = self._url(caminho_ou_url)
        WebDriverWait(self._navegador, timeout).until(
            lambda drv: drv.current_url == url_esperada
        )
        return self._navegador.current_url

    def url_atual(self) -> str:
        return self._navegador.current_url

    def esta_na_rota(self, caminho: str) -> bool:
        return caminho in self._navegador.current_url

    def _preencher(self, localizador: tuple[str, str], valor: str) -> None:
        campo = self._navegador.find_element(*localizador)
        campo.clear()
        campo.send_keys(valor)