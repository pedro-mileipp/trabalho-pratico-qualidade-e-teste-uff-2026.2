"""Page object da tela de Transferência PIX (``/pix``).

Os seletores ficam concentrados aqui: se a tela mudar, só o page object precisa ser ajustado.
Os campos são localizados pelo ``id`` (incluídos na issue #48, junto com o ``for`` dos rótulos).
O saldo e o extrato são lidos no dashboard (``/``), para onde o fluxo aprovado redireciona.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

ESPERA_SEGUNDOS = 5


class PaginaPix:
    CAMINHO = "/pix"
    CAMPO_CHAVE = (By.ID, "chave")
    CAMPO_TIPO = (By.ID, "tipo")
    CAMPO_VALOR = (By.ID, "valor")
    BOTAO_TRANSFERIR = (By.CSS_SELECTOR, "form button[type='submit']")
    FLASH = (By.CSS_SELECTOR, ".flash")
    PARAGRAFO_SALDO = (By.CSS_SELECTOR, ".cartao p")

    def __init__(self, navegador: WebDriver, servidor: str) -> None:
        self._navegador = navegador
        self._servidor = servidor

    def abrir(self) -> PaginaPix:
        self._navegador.get(self._servidor + self.CAMINHO)
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.CAMPO_CHAVE)
        )
        return self

    def preencher(self, chave: str, tipo: str, valor: str) -> None:
        self._navegador.find_element(*self.CAMPO_CHAVE).send_keys(chave)
        Select(self._navegador.find_element(*self.CAMPO_TIPO)).select_by_value(tipo)
        self._navegador.find_element(*self.CAMPO_VALOR).send_keys(valor)

    def enviar(self) -> None:
        self._navegador.find_element(*self.BOTAO_TRANSFERIR).click()

    def mensagem_flash(self) -> str:
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.FLASH)
        )
        return self._navegador.find_element(*self.FLASH).text

    def tem_flash(self) -> bool:
        return bool(self._navegador.find_elements(*self.FLASH))

    def campo_abaixo_do_minimo(self, nome_campo: str) -> bool:
        """True se o navegador barrou o campo pela validação HTML5 ``min`` (rangeUnderflow)."""
        campo = self._navegador.find_element(By.ID, nome_campo)
        return self._navegador.execute_script("return arguments[0].validity.rangeUnderflow;", campo)

    def dados_dashboard(self) -> tuple[float, list[str]]:
        """Abre o dashboard e devolve (saldo, linhas do extrato)."""
        self._navegador.get(self._servidor + "/")
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.PARAGRAFO_SALDO)
        )
        texto_saldo = self._navegador.find_element(*self.PARAGRAFO_SALDO).text
        saldo = float(texto_saldo.split("R$")[1].strip())
        linhas = [
            linha.text
            for linha in self._navegador.find_elements(By.CSS_SELECTOR, "table tr")
        ][1:]  # a primeira linha é o cabeçalho
        return saldo, linhas
