# Trabalho Prático — Qualidade e Teste (UFF 2026.2)

Repositório do trabalho prático da disciplina **Qualidade e Teste** (UFF 2026.2), sobre o **Banco Digital**.

## Sobre o projeto

O Banco Digital é uma aplicação web em **Python + Flask + SQLite** com login e serviços bancários simulados. As regras de negócio ficam em classes de domínio puras (PIX, juros, tarifas, empréstimo e crédito), uma por integrante, com **CC ≥ 10**, o que permite testá-las sem o framework.

O trabalho foi dividido em duas entregas: a primeira com testes unitários e casos manuais; a segunda com integração, testes de sistema, cobertura estrutural, mutação, inspeção estática e requisito não funcional de segurança. O escopo e os critérios estão no **[Plano de Teste](docs/plano_de_teste.md)** — também disponível em **[DOCX/Google Docs](https://docs.google.com/document/d/1LWiJPPQAZKMw0ycTe8bxu5VSc6Tf0NlNcL60BzXTZOg/edit?usp=sharing)**.

A arquitetura e os módulos estão em **[docs/aplicacao.md](docs/aplicacao.md)**.

## Artefatos

| Artefato | Link |
|---|---|
| Plano de Teste | [Markdown](docs/plano_de_teste.md) · [DOCX/Google Docs](https://docs.google.com/document/d/1LWiJPPQAZKMw0ycTe8bxu5VSc6Tf0NlNcL60BzXTZOg/edit?usp=sharing) |
| Plano de Projeto | [docs/plano_projeto.md](docs/plano_projeto.md) |
| Documentação da aplicação | [docs/aplicacao.md](docs/aplicacao.md) |
| Relatório de cobertura e mutação | [docs/relatorios/cobertura_mutacao.md](docs/relatorios/cobertura_mutacao.md) |
| Inspeção SonarQube | [docs/relatorios/inspecao_sonar.md](docs/relatorios/inspecao_sonar.md) |
| RNF de segurança (RNF06) | [docs/relatorios/rnf_seguranca.md](docs/relatorios/rnf_seguranca.md) |
| Avaliação ISO/IEC 25010 | [docs/relatorios/iso25010.md](docs/relatorios/iso25010.md) |
| Registro de uso de IA | [docs/ai/AI-LOG.md](docs/ai/AI-LOG.md) |
| Casos de teste manuais | [tests/testes_manuais/](tests/testes_manuais/) |
| Relatório do TestLink (Auth) | [PDF](https://drive.google.com/file/d/14yShZiduI8gixsV5wCQqA70DH2TV4SN4/view?usp=sharing) |
| Evidências de execução | [docs/relatorios/evidencias/](docs/relatorios/evidencias/) |
| Issues e milestones | [GitHub Issues](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues) |
| Enunciado | [docs/descricao_trabalho.md](docs/descricao_trabalho.md) |

Os resultados e as evidências de execução ficam nos relatórios de [cobertura e mutação](docs/relatorios/cobertura_mutacao.md) e [inspeção SonarQube](docs/relatorios/inspecao_sonar.md).

## Como executar

Requisito: [uv](https://docs.astral.sh/uv/) (gerencia a versão do Python e as dependências).

```bash
uv sync --all-extras
uv run flask --app app:create_app run
```

Acesse `http://127.0.0.1:5000` e crie uma conta em `/registro`. A versão do Python é fixada em `.python-version` e as dependências em `pyproject.toml` (travadas em `uv.lock`).

## Testes

| Suíte | Comando | Onde |
|---|---|---|
| Unitários | `uv run pytest tests/unit` | [`tests/unit/`](tests/unit/) |
| Integração | `uv run pytest tests/integration` | [`tests/integration/`](tests/integration/) |
| Sistema (Selenium) | `uv run pytest tests/system` | [`tests/system/`](tests/system/) |
| Requisitos não funcionais | `uv run pytest tests/rnf` | [`tests/rnf/`](tests/rnf/) |
| Completa | `uv run pytest` | [`tests/`](tests/) |

Cobertura e mutação:

```bash
uv run pytest --cov --cov-branch --cov-report=term-missing
uv run mutmut run --max-children 8
```

Lint e complexidade:

```bash
uv run ruff check app/
uv run radon cc app/dominio -s
```

Para os testes de sistema, o Chrome é necessário; o driver é resolvido pelo Selenium Manager.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `app/` | Domínio, repositórios, serviços e camada web |
| `tests/` | Unitários, integração, sistema, RNF e casos manuais |
| `docs/` | Plano, relatórios, AI-LOG e documentação |
| `scripts/` | Automação do SonarQube local |

## Contribuidores

- [alexandrelimaxs](https://github.com/alexandrelimaxs)
- [danielizu](https://github.com/danielizu)
- [pedro-mileipp](https://github.com/pedro-mileipp)
- [n2Gabrielle](https://github.com/n2Gabrielle)
- [ViniciusFelinto](https://github.com/ViniciusFelinto)
