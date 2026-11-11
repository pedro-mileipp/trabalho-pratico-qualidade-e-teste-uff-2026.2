# AGENTS.md

Banco Digital — trabalho prático de Qualidade e Teste (UFF 2026.2). App Flask em Python, projetado para as técnicas de teste da disciplina.

## Tooling (não pule)

- Gerenciador de pacotes: **uv** (nunca pip/requirements.txt). Python 3.12 fixado em `.python-version`; deps em `pyproject.toml` (trava em `uv.lock`).
- Instalar/env: `uv sync --all-extras`. Rodar qualquer coisa com `uv run ...`.
- Rodar o app: `uv run flask --app app:create_app run`. É uma app factory — não existe `app.py`.
- Lint: `uv run ruff check app/`. Medir complexidade: `uv run radon cc app/dominio -s`.

## Estado do projeto

- Testes unitários em `tests/unit/` (1 arquivo por classe de domínio) e casos manuais em `tests/testes_manuais/`. Config do pytest em `pyproject.toml` (`[tool.pytest.ini_options]`). **Ainda não há CI** (sem `.github/workflows/`). As dev deps (pytest, pytest-mock, pytest-cov, selenium, webdriver-manager, mutmut, radon) estão em `pyproject.toml`.
- Resultados de cobertura/mutação por classe: `docs/relatorios/cobertura_mutacao.md`.
- Testes de sistema (Selenium, Chrome headless) em `tests/system/`, **uma pasta por funcionalidade** (ex.: `tests/system/credito/`) com `test_<funcionalidade>_sistema.py` e o page object `pagina_<funcionalidade>.py`. Reutilize as fixtures `servidor`, `navegador`, `cliente_logado` e `evidencia` (print de uma etapa, ex.: `evidencia("formulario_preenchido")`) de `tests/system/conftest.py`. Os nomes de arquivo não podem se repetir entre pastas (não há `__init__.py`), por isso o sufixo `_sistema` e o prefixo `pagina_`. `EVIDENCIAS=1` salva screenshots em `<funcionalidade>/evidencias/`; falhas vão para `<funcionalidade>/falhas/` (fora do git).
- Testes de requisitos não funcionais em `tests/rnf/`, **uma pasta por requisito** (ex.: `tests/rnf/seguranca/`), com o cliente de testes do Flask (sem navegador) e banco temporário por teste (fixtures `app`, `cliente_http`, `banco`, `cliente_cadastrado` em `tests/rnf/conftest.py`). Não importe `conftest` nos testes: há mais de um `conftest.py` no projeto. Resultados de segurança em `docs/relatorios/rnf_seguranca.md`.
- A implementação de testes é o trabalho dos integrantes. **Não crie arquivos de teste** a menos que explicitamente solicitado.

## Arquitetura

Camadas (importações só de cima para baixo): `app/web` → `app/servicos` → `app/dominio`; `app/repositorios` é injetado nos serviços.

- `app/dominio/` — regras puras, **proibido importar Flask**. Classes sob teste; alvo de cobertura/mutação.
- `app/repositorios/` — ABC `Repositorio` + `SqliteRepositorio` + `MemoriaRepositorio`. Serviços recebem o repositório por injeção (base para mocks).
- `app/servicos/` — orquestração (auth, transações).
- `app/web/` — blueprints Flask; **templates ficam em `app/templates/`** (pasta padrão), não em `app/web/`.

## Gotchas (fáceis de errar)

- `SqliteRepositorio` **não fecha conexões** (vem de `get_db()` do Flask `g`, fechadas no teardown). Não adicione `conn.close()`.
- **CC ≥ 10 por módulo de domínio é requisito da disciplina.** Mantenha os `if`/laços que geram complexidade; o ruff ignora `PLR1730`/`DTZ005` de propósito — não "corrija" essas regras nem reescreva os branches com `max/min` que reduzam o CC.
- Hash de senha usa `method="pbkdf2:sha256"` explicitamente (compat com Python 3.9 sem `hashlib.scrypt`). Não remova.
- Smoke test: defina `DATABASE=/tmp/....db` para não criar `banco.db` no workspace.

## Convenções

- Commits no estilo conventional: `feat:`, `docs:`, `chore:` etc. PRs são abertos contra `main` via `gh`.
- Docs do projeto: `docs/plano_projeto.md` (planejamento/entregas) e `docs/aplicacao.md` (arquitetura). O README lista todos os artefatos — atualize-o quando criar novos.