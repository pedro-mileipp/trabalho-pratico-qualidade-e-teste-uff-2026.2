"""Page object da tela de Análise de Crédito (``/credito``).

Os seletores ficam concentrados aqui: se a tela mudar, só o page object precisa ser ajustado.
Os templates não têm ``id`` nos elementos, então os campos são localizados pelo ``name`` e o
resultado pela estrutura do cartão (``.cartao h3`` / parágrafos seguintes).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ESPERA_SEGUNDOS = 5


@dataclass(frozen=True)
class ResultadoCreditoTela:
    situacao: str
    score: int
    limite: float
    motivo: str


class PaginaCredito:
    CAMINHO = "/credito"
    CAMPO_RENDA = (By.NAME, "renda")
    CAMPO_VALOR = (By.NAME, "valor")
    BOTAO_ANALISAR = (By.CSS_SELECTOR, "form button[type='submit']")
    TITULO_RESULTADO = (By.CSS_SELECTOR, ".cartao h3")
    PARAGRAFOS_RESULTADO = (By.CSS_SELECTOR, ".cartao h3 ~ p")
    _DETALHES = re.compile(r"Score:\s*(\d+)\s*·\s*Limite:\s*R\$\s*([\d.]+)\s*·\s*Motivo:\s*(\w+)")

    def __init__(self, navegador: WebDriver, servidor: str) -> None:
        self._navegador = navegador
        self._servidor = servidor

    def abrir(self) -> PaginaCredito:
        self._navegador.get(self._servidor + self.CAMINHO)
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.CAMPO_RENDA)
        )
        return self

    def analisar(self, renda: float | str, valor: float | str) -> None:
        self._preencher(self.CAMPO_RENDA, renda)
        self._preencher(self.CAMPO_VALOR, valor)
        self._navegador.find_element(*self.BOTAO_ANALISAR).click()

    def resultado(self) -> ResultadoCreditoTela:
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.TITULO_RESULTADO)
        )
        situacao_texto, detalhes_texto = (
            p.text for p in self._navegador.find_elements(*self.PARAGRAFOS_RESULTADO)
        )
        detalhes = self._DETALHES.search(detalhes_texto)
        assert detalhes is not None, f"resultado em formato inesperado: {detalhes_texto!r}"
        return ResultadoCreditoTela(
            situacao=situacao_texto.split(":", 1)[1].strip(),
            score=int(detalhes.group(1)),
            limite=float(detalhes.group(2)),
            motivo=detalhes.group(3),
        )

    def tem_resultado(self) -> bool:
        return bool(self._navegador.find_elements(*self.TITULO_RESULTADO))

    def campo_abaixo_do_minimo(self, nome_campo: str) -> bool:
        """True se o navegador barrou o campo pela validação HTML5 ``min`` (rangeUnderflow)."""
        campo = self._navegador.find_element(By.NAME, nome_campo)
        return self._navegador.execute_script("return arguments[0].validity.rangeUnderflow;", campo)

    def _preencher(self, localizador: tuple[str, str], valor: float | str) -> None:
        campo = self._navegador.find_element(*localizador)
        campo.clear()
        campo.send_keys(str(valor))
