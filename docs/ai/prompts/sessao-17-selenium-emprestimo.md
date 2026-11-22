# Sessão 17 — Testes de sistema Selenium para Empréstimo (issue #59)

| Campo | Valor |
|---|---|
| Responsável | Vinicius Sales Felinto (`ViniciusFelinto`) |
| Data | 22/11/2026 |
| Ferramenta | Google Antigravity (modelos `Claude Opus 4.6 Thinking` e `Gemini 3.8 Flash`) / Terminal (`uv run pytest`) |
| Atividade | Automatizar testes de sistema com Selenium para Empréstimo (RF05 — issue #59) |
| Artefatos | `tests/system/emprestimo/pagina_emprestimo.py`, `tests/system/emprestimo/test_emprestimo_sistema.py`, `tests/system/emprestimo/evidencias/` |

## Contexto

Automatizar os cenários de sistema da funcionalidade de Simulação de Empréstimo (`/emprestimo`), cobrindo o requisito funcional RF05 para a issue #59. A implementação toma como referência os casos manuais em `tests/testes_manuais/emprestimo/caso_emprestimo.md` (TC-01 a TC-05), as fixtures compartilhadas de `tests/system/conftest.py` (servidor Flask real em thread com porta livre, banco SQLite isolado por execução, Chrome headless via Selenium Manager, criação de usuário único via `cliente_logado` e captura de evidências via `evidencia`) e o padrão de Page Object estabelecido em `tests/system/credito/`.

## Prompt utilizado

> "Você é um testador experiente com conhecimento nas melhores práticas do mercado sobre teste de softwares, sabendo disso, faça o teste de sistema abaixo usando selenium no meu projeto, siga extritamente o que o md diz e siga o padrão PageObject que é utilizado em java, mas adaptando para o cenário do python. Segue abaixo o md do que é necessário:
>
> ## Objetivo
> Automatizar o fluxo de Empréstimo com Selenium, cobrindo o requisito funcional RF05.
>
> ## Contexto
> - O enunciado exige testes de sistema com Selenium.
> - Caso manual de referência: `tests/testes_manuais/emprestimo/`.
> - Usar a fixture base do Selenium (Flask em thread, porta livre, banco temporário) criada na A1.
> - Chrome headless; Selenium Manager ou webdriver-manager.
>
> ## O que fazer
> 1. Criar o cenário em `tests/system/`.
> 2. Cobrir o fluxo principal e pelo menos um fluxo de recusa: Price e SAC aprovados; recusas por valor mínimo, prazo e comprometimento da renda.
> 3. Usar seletores estáveis (IDs/names), evitando XPath frágil.
> 4. Salvar screenshot/HTML em caso de falha.
> 5. Garantir independência entre testes e banco limpo.
>
> ## Critérios de aceite
> - [ ] Cenário automatizado cobrindo o requisito funcional.
> - [ ] `uv run pytest tests/system -q` verde.
> - [ ] Evidência em caso de falha.
> - [ ] Teste determinístico e independente."

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações quando a IA é usada na geração de testes.

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| Criação inicial do Page Object `PaginaEmprestimo` e do arquivo de testes `test_emprestimo_sistema.py` planejando validar o motivo `comprometimento_acima` no TC-05 e submissão direta do prazo 1 mês no TC-04. | `PaginaEmprestimo` e `test_emprestimo_sistema.py` totalmente alinhados ao comportamento real da interface e do domínio, com **6 casos aprovados** na suíte de empréstimo e **31 casos aprovados** na suíte geral de sistema (`tests/system`). | 1. **Análise do TC-05 (Comprometimento de Renda vs. Teto):** A regra de domínio em `SimuladorEmprestimo.simular()` avalia o teto da faixa (`principal > teto_por_renda(renda)`) antes do comprometimento da parcela. Para renda de R$ 1.000,00, o teto é R$ 150,00 (15%). O valor solicitado de R$ 200,00 excede esse teto, resultando em `acima_teto`. A conferência da evidência manual original (`tests/testes_manuais/emprestimo/evidencias/evidenciastc05-comprometimento-renda.png`) comprovou que a tela exibiu `"Não aprovado: acima_teto"`. O teste automatizado foi alinhado a essa asserção real.<br>2. **Análise do TC-04 (Validação HTML5 do Prazo):** O input `meses` no template possui atributo nativo `min="2"`. Em conformidade com o screenshot do caso manual (`evidenciastc04-prazo-invalido.png`), o Chrome headless bloqueia o envio exibindo o tooltip nativo (`rangeUnderflow`), sem disparar o POST. Implementado o método `campo_abaixo_do_minimo("meses")` via JavaScript `validity.rangeUnderflow` (seguindo o padrão já adotado em `tests/system/credito/test_credito_sistema.py`).<br>3. **Qualidade e Linting (Ruff):** Ajustado type hint de `_preencher_campo` de `float | int | str` para `float | str` (`PYI041`) e ordenação de imports (`I001`). |

**Decisão:** Mantida estrita aderência ao comportamento real das telas e regras de negócio da aplicação, sem alterar os templates ou o código de domínio. A suíte foi integrada à infraestrutura de testes de sistema existente em `conftest.py`.

**Validação inicial:**
- Execução isolada de `tests/system/emprestimo`: `6 passed in 15.51s`.
- Execução com lint: 2 avisos de estilo corrigidos via `uv run ruff check --fix`.

**Validação final:**
- `uv run pytest tests/system -q` → `31 passed in 49.36s` (e reexecução em `53.05s`).
- `EVIDENCIAS=1 uv run pytest tests/system/emprestimo -q` → `6 passed in 12.60s` gerando screenshots ordenados por etapa em `tests/system/emprestimo/evidencias/`.
- `uv run ruff check tests/system/emprestimo/` → `All checks passed!`.

## Ações executadas

1. **Inspeção e pesquisa da funcionalidade:**
   - Leitura do caso manual de referência em `tests/testes_manuais/emprestimo/caso_emprestimo.md`.
   - Inspeção visual das evidências em PNG originais (`evidenciastc01` a `evidenciastc05`).
   - Leitura das regras de negócio em `app/dominio/emprestimo.py` e da rota Flask em `app/web/routes/emprestimo.py`.
   - Inspeção do formulário em `app/templates/emprestimo.html`, identificando nomes estáveis dos campos (`principal`, `meses`, `renda`, `sistema`) e ausência de IDs.
   - Análise do padrão de Page Object e testes de sistema de referência em `tests/system/credito/` e fixtures em `tests/system/conftest.py`.

2. **Implementação do Page Object (`tests/system/emprestimo/pagina_emprestimo.py`):**
   - Criação da classe `PaginaEmprestimo` com constantes de caminho (`/emprestimo`) e seletores baseados em `By.NAME` e `By.CSS_SELECTOR`.
   - Dataclasses imutáveis `ResultadoEmprestimoTela` e `RecusaEmprestimoTela` para representação tipada dos retornos da tela.
   - Métodos de interação: `abrir()`, `preencher()`, `enviar()`, `resultado_aprovado()`, `resultado_recusado()`, `tem_resultado()` e `campo_abaixo_do_minimo()`.

3. **Implementação da suíte de testes (`tests/system/emprestimo/test_emprestimo_sistema.py`):**
   - `test_simulacao_aprovada`: Parametrizado para Tabela Price (TC-01: R$ 100,46 / R$ 1.205,52) e SAC (TC-02: R$ 113,33 / R$ 1.194,96).
   - `test_recusa_valor_abaixo_minimo`: Simulação com valor R$ 50,00 resultando em recusa por `valor_abaixo_minimo` (TC-03).
   - `test_prazo_abaixo_do_minimo_barrado_pelo_formulario`: Prazo de 1 mês barrado na interface por `rangeUnderflow` HTML5, sem submissão indevida (TC-04).
   - `test_recusa_acima_teto_renda`: Renda R$ 1.000,00 e valor R$ 200,00 (teto R$ 150,00) gerando recusa por `acima_teto` (TC-05).
   - `test_emprestimo_exige_login`: Garantia de proteção de rota redirecionando usuários não autenticados para `/login`.

4. **Validação e evidências:**
   - Execução de toda a suíte de sistema (`tests/system`) garantindo determinismo e ausência de regressão.
   - Validação da geração de screenshots com `EVIDENCIAS=1`.
   - Verificação e aprovação com `ruff check`.

## Resultado

- **6 testes de sistema de empréstimo criados e aprovados** em `tests/system/emprestimo/`.
- Suíte geral de sistema com **31 testes verdes** (`uv run pytest tests/system -q`).
- Independência total entre execuções através do isolamento de cada teste com a fixture `cliente_logado`.
- Suporte a geração de evidências automáticas em falhas (`falhas/`) e durante execução auditada (`evidencias/`).
