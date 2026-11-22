"""Page object da tela de Consulta de Tarifas (``/tarifas``).

Os seletores ficam concentrados aqui: se a tela mudar, só o page object precisa ser ajustado.
Os campos são localizados pelo ``id`` (``tipo``, ``saldo`` e ``transacoes`` vieram da issue #50;
``pacote`` e ``tarifa-resultado`` foram incluídos na issue #58).
"""

from __future__ import annotations

import re

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

ESPERA_SEGUNDOS = 5


class PaginaTarifas:
    CAMINHO = "/tarifas"
    CAMPO_TIPO = (By.ID, "tipo")
    CAMPO_SALDO = (By.ID, "saldo")
    CAMPO_TRANSACOES = (By.ID, "transacoes")
    CAMPO_PACOTE = (By.ID, "pacote")
    BOTAO_CALCULAR = (By.CSS_SELECTOR, "form button[type='submit']")
    RESULTADO = (By.ID, "tarifa-resultado")
    _VALOR = re.compile(r"R\$\s*(-?[\d.]+)")

    def __init__(self, navegador: WebDriver, servidor: str) -> None:
        self._navegador = navegador
        self._servidor = servidor

    def abrir(self) -> PaginaTarifas:
        self._navegador.get(self._servidor + self.CAMINHO)
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.CAMPO_TIPO)
        )
        return self

    def preencher(self, tipo: str, saldo: float | str, transacoes: int | str, pacote: bool) -> None:
        Select(self._navegador.find_element(*self.CAMPO_TIPO)).select_by_value(tipo)
        self._preencher(self.CAMPO_SALDO, saldo)
        self._preencher(self.CAMPO_TRANSACOES, transacoes)
        caixa = self._navegador.find_element(*self.CAMPO_PACOTE)
        if caixa.is_selected() != pacote:
            caixa.click()

    def enviar(self) -> None:
        self._navegador.find_element(*self.BOTAO_CALCULAR).click()

    def tarifa_exibida(self) -> float:
        resultado = WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.RESULTADO)
        )
        valor = self._VALOR.search(resultado.text)
        assert valor is not None, f"resultado em formato inesperado: {resultado.text!r}"
        return float(valor.group(1))

    def tem_resultado(self) -> bool:
        # Sem espera: nos testes de recusa o resultado não deve aparecer, e esperar só atrasaria o teste.
        return bool(self._navegador.find_elements(*self.RESULTADO))

    def campo_abaixo_do_minimo(self, id_campo: str) -> bool:
        """True se o navegador barrou o campo pela validação HTML5 ``min`` (rangeUnderflow)."""
        campo = self._navegador.find_element(By.ID, id_campo)
        return self._navegador.execute_script("return arguments[0].validity.rangeUnderflow;", campo)

    def _preencher(self, localizador: tuple[str, str], valor: float | str | int) -> None:
        campo = self._navegador.find_element(*localizador)
        campo.clear()
        campo.send_keys(str(valor))
