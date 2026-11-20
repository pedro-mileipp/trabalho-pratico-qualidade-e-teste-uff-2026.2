# Sessão 16 — Testes de sistema Selenium para Autenticação (issue #57)

| Campo | Valor |
|---|---|
| Responsável | Gabrielle Rosa (`n2Gabrielle`) |
| Data | 20/11/2026 |
| Ferramenta | Gemini / VS Code / Terminal (`.venv/bin/pytest`) |
| Atividade | Automatizar testes de sistema com Selenium para Autenticação (RF01/RF02 — issue #57) |
| Artefatos | `tests/system/auth/pagina_auth.py`, `tests/system/auth/test_auth_sistema.py`, `tests/system/auth/evidencias/` |

## Contexto

Automatizar os cenários de sistema da funcionalidade de Autenticação (`/registro`, `/login`, `/logout` e rotas protegidas) cobrindo os requisitos funcionais RF01/RF02 para a issue #57, tomando como referência os casos manuais em `tests/testes_manuais/auth/caso_auth.md`, as fixtures de `tests/system/conftest.py` (Flask em thread, porta livre, banco SQLite temporário, Chrome headless e `evidencia`) e o padrão de Page Object e testes parametrizados de `tests/system/credito/`.

## Prompt utilizado

> 1. "Com base nos arquivos `app/templates/login.html`, `app/templates/registro.html`, `app/web/routes/auth.py` e no padrão de `tests/system/credito/pagina_credito.py`, crie o Page Object `PaginaAuth` em `tests/system/auth/pagina_auth.py` usando `WebDriverWait`, seletores estáveis por `By.ID` / `By.NAME` / `By.CSS_SELECTOR` (sem XPath frágil) e métodos para abrir `/registro`, `/login` e rotas protegidas, preencher formulários, submeter e ler mensagens ou redirecionamentos."
>
> 2. "Com base em `tests/testes_manuais/auth/`, `tests/system/conftest.py`, `tests/system/auth/pagina_auth.py` e no estilo de `tests/system/credito/test_credito_sistema.py`, crie `tests/system/auth/test_auth_sistema.py` cobrindo RF01/RF02 com `@pytest.mark.parametrize`: cadastro válido e inválido, login válido e inválido, logout, acesso a rota protegida sem autenticação e uso da fixture `evidencia(...)` quando solicitado. Garanta independência total entre os testes e compatibilidade com `uv run pytest tests/system -q` em Chrome headless."

**Resposta da IA:** gerou o Page Object `PaginaAuth` em `tests/system/auth/pagina_auth.py` e a suíte `tests/system/auth/test_auth_sistema.py` (25 testes no total, cobrindo cadastro válido/inválido, login válido/inválido, logout e rotas protegidas com e-mails únicos e independência entre cenários).

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações quando a IA é usada na geração de testes.

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| `PaginaAuth` e `test_auth_sistema.py` gerados (25 casos), com 2 falhas na primeira execução (`test_cadastro_valido_e_redirecionamento_para_dashboard` e `test_cadastro_invalido_parametrizado[email_duplicado]`) e `StaleElementReferenceException` na segunda execução devido a sincronização de URL e leitura de elementos flash durante transição de DOM | `PaginaAuth` e `test_auth_sistema.py` estabilizados com **25 casos aprovados** em execuções repetidas em Chrome headless e evidências geradas em `tests/system/auth/evidencias/` | Em `aguardar_redirecionamento`, passou a aguardar a URL completa (`self._url(caminho_ou_url)`) em vez de `alvo in drv.current_url` (evitando que `"/"` casasse prematuramente com `"/registro"`); em `submeter()`, adicionou espera de `document.readyState == "complete"`; em `mensagens()` e `mensagem_flash()`, adicionou espera com `WebDriverWait` e tratamento de `StaleElementReferenceException` |

**Decisão:** todas as falhas iniciais foram classificadas como problemas de sincronização/espera no Page Object e nos testes (e não defeitos na aplicação de autenticação), sendo corrigidas em `tests/system/auth/pagina_auth.py`; o código de aplicação e as fixtures em `tests/system/conftest.py` foram mantidos sem alterações.

**Validação inicial:** `.venv/bin/pytest tests/system -q` → `2 failed, 23 passed in 25.59s` (e `1 failed, 24 passed in 16.07s` com `StaleElementReferenceException` antes do tratamento).

**Validação final:** `.venv/bin/pytest tests/system -q` → `25 passed in 20.53s` e reexecução `25 passed in 17.06s`; evidências geradas em `tests/system/auth/evidencias/` com `EVIDENCIAS=1`.

## Ações executadas

1. Consultados `app/templates/login.html`, `app/templates/registro.html`, `app/web/routes/auth.py`, `tests/testes_manuais/auth/caso_auth.md`, `tests/system/conftest.py` e `tests/system/credito/`.
2. Criados `tests/system/auth/pagina_auth.py` e `tests/system/auth/test_auth_sistema.py` na branch `test/issue-57-selenium-auth`.
3. Executada `.venv/bin/pytest tests/system -q` e diagnosticadas as falhas de redirecionamento e `StaleElementReferenceException` na leitura de mensagem flash.
4. Ajustados `aguardar_redirecionamento`, `submeter`, `mensagens` e `mensagem_flash` em `tests/system/auth/pagina_auth.py`, reexecutada a suíte completa (`25 passed` em execuções consecutivas) e gerados os screenshots em `tests/system/auth/evidencias/` com `EVIDENCIAS=1`.

## Resultado

- **25 casos aprovados** em `tests/system` (`20.53s` / `17.06s`), sem dependência entre testes ou necessidade de intervenção manual.
- Cobertura dos fluxos de cadastro válido/inválido, login válido/inválido, logout, acesso sem sessão a rotas protegidas (`/`, `/credito`) e suporte à fixture `evidencia(...)`, com screenshots salvos em `tests/system/auth/evidencias/`.
- Nenhum defeito novo aberto a partir da suíte de sistema de autenticação.