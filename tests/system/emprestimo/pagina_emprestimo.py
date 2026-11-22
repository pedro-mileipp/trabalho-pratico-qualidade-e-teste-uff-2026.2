"""Page object da tela de Simulação de Empréstimo (``/emprestimo``).

Os seletores ficam concentrados aqui: se a tela mudar, só o page object precisa ser ajustado.
Os campos são localizados pelo ``name`` e o resultado pela estrutura do cartão
(``.cartao h3`` / parágrafos seguintes).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

ESPERA_SEGUNDOS = 5


@dataclass(frozen=True)
class ResultadoEmprestimoTela:
    """Dados extraídos da seção Resultado visível na tela."""

    aprovado: bool
    primeira_parcela: float
    total: float
    numero_parcelas: int


@dataclass(frozen=True)
class RecusaEmprestimoTela:
    """Dados de uma simulação recusada."""

    motivo: str


class PaginaEmprestimo:
    CAMINHO = "/emprestimo"

    # --- seletores estáveis (name / CSS) ---
    CAMPO_PRINCIPAL = (By.NAME, "principal")
    CAMPO_MESES = (By.NAME, "meses")
    CAMPO_RENDA = (By.NAME, "renda")
    CAMPO_SISTEMA = (By.NAME, "sistema")
    BOTAO_SIMULAR = (By.CSS_SELECTOR, "form button[type='submit']")
    TITULO_RESULTADO = (By.CSS_SELECTOR, ".cartao h3")
    PARAGRAFOS_RESULTADO = (By.CSS_SELECTOR, ".cartao h3 ~ p")

    _RE_APROVADO = re.compile(
        r"1ª parcela:\s*R\$\s*([\d.,]+)\s*·\s*Total:\s*R\$\s*([\d.,]+)"
    )
    _RE_PARCELAS = re.compile(r"(\d+)\s*parcelas")
    _RE_RECUSA = re.compile(r"Não aprovado:\s*(\S+)")

    def __init__(self, navegador: WebDriver, servidor: str) -> None:
        self._navegador = navegador
        self._servidor = servidor

    # --- ações ---

    def abrir(self) -> PaginaEmprestimo:
        self._navegador.get(self._servidor + self.CAMINHO)
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.CAMPO_PRINCIPAL)
        )
        return self

    def preencher(
        self,
        principal: float | str,
        meses: int | str,
        renda: float | str,
        sistema: str = "price",
    ) -> None:
        self._preencher_campo(self.CAMPO_PRINCIPAL, principal)
        self._preencher_campo(self.CAMPO_MESES, meses)
        self._preencher_campo(self.CAMPO_RENDA, renda)
        Select(self._navegador.find_element(*self.CAMPO_SISTEMA)).select_by_value(
            sistema
        )

    def enviar(self) -> None:
        self._navegador.find_element(*self.BOTAO_SIMULAR).click()

    # --- leitura de resultado ---

    def tem_resultado(self) -> bool:
        return bool(self._navegador.find_elements(*self.TITULO_RESULTADO))

    def resultado_aprovado(self) -> ResultadoEmprestimoTela:
        """Extrai os dados de uma simulação aprovada."""
        self._aguardar_resultado()
        paragrafos = self._navegador.find_elements(*self.PARAGRAFOS_RESULTADO)
        texto_completo = " ".join(p.text for p in paragrafos)

        match_aprovado = self._RE_APROVADO.search(texto_completo)
        assert match_aprovado is not None, (
            f"Resultado aprovado em formato inesperado: {texto_completo!r}"
        )

        match_parcelas = self._RE_PARCELAS.search(texto_completo)
        assert match_parcelas is not None, (
            f"Número de parcelas não encontrado: {texto_completo!r}"
        )

        return ResultadoEmprestimoTela(
            aprovado=True,
            primeira_parcela=float(match_aprovado.group(1)),
            total=float(match_aprovado.group(2)),
            numero_parcelas=int(match_parcelas.group(1)),
        )

    def resultado_recusado(self) -> RecusaEmprestimoTela:
        """Extrai o motivo de uma simulação recusada."""
        self._aguardar_resultado()
        paragrafos = self._navegador.find_elements(*self.PARAGRAFOS_RESULTADO)
        texto_completo = " ".join(p.text for p in paragrafos)

        match_recusa = self._RE_RECUSA.search(texto_completo)
        assert match_recusa is not None, (
            f"Resultado de recusa em formato inesperado: {texto_completo!r}"
        )

        return RecusaEmprestimoTela(motivo=match_recusa.group(1))

    def texto_resultado(self) -> str:
        """Retorna o texto bruto da seção resultado (aprovado ou recusado)."""
        self._aguardar_resultado()
        paragrafos = self._navegador.find_elements(*self.PARAGRAFOS_RESULTADO)
        return " ".join(p.text for p in paragrafos)

    # --- helpers internos ---

    def _aguardar_resultado(self) -> None:
        WebDriverWait(self._navegador, ESPERA_SEGUNDOS).until(
            EC.presence_of_element_located(self.TITULO_RESULTADO)
        )

    def campo_abaixo_do_minimo(self, nome_campo: str) -> bool:
        """True se o navegador barrou o campo pela validação HTML5 ``min`` (rangeUnderflow)."""
        campo = self._navegador.find_element(By.NAME, nome_campo)
        return self._navegador.execute_script(
            "return arguments[0].validity.rangeUnderflow;", campo
        )

    def _preencher_campo(
        self, localizador: tuple[str, str], valor: float | str
    ) -> None:
        campo = self._navegador.find_element(*localizador)
        campo.clear()
        campo.send_keys(str(valor))
