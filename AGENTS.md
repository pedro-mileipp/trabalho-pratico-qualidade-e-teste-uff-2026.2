# AGENTS.md

Banco Digital — trabalho prático de Qualidade e Teste (UFF 2026.2). App Flask em Python, projetado para as técnicas de teste da disciplina.

## Tooling (não pule)

- Gerenciador de pacotes: **uv** (nunca pip/requirements.txt). Python 3.12 fixado em `.python-version`; deps em `pyproject.toml` (trava em `uv.lock`).
- Instalar/env: `uv sync --all-extras`. Rodar qualquer coisa com `uv run ...`.
- Rodar o app: `uv run flask --app app:create_app run`. É uma app factory — não existe `app.py`.
- Lint: `uv run ruff check app/`. Medir complexidade: `uv run radon cc app/dominio -s`.

## Estado do projeto

- **Não há testes nem CI ainda** (sem `tests/`, `pytest.ini`, workflows). As dev deps (pytest, pytest-mock, pytest-cov, selenium, webdriver-manager, mutmut, radon) já estão declaradas em `pyproject.toml`.
- A implementação de testes é o trabalho dos integrantes. **Não crie arquivos de teste** a menos que explicitamente solicitado.
- O código de domínio contém **defeitos naturais propositais** para os testes revelarem. `docs/defeitos_conhecidos.md` lista os defeitos conhecidos, **é gitignored e nunca deve ser commitado**.

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