# Trabalho Prático — Qualidade e Teste (UFF 2026.2)

Repositório do trabalho prático da disciplina **Qualidade e Teste** (UFF 2026.2).

## Sobre o trabalho

O grupo aplica os conceitos aprendidos na disciplina Qualidade e Teste sobre um software livre desenvolvido por nós — o **Banco Digital**. O objetivo é exercitar as técnicas de teste de software em um sistema real, com duas entregas:

### Entrega 1 (peso 3)
- Descrição do escopo no **[Plano de Teste](docs/plano_de_teste.md)**
- Testes unitários de pelo menos uma classe não-CRUD por integrante
- Casos de teste manuais (uma funcionalidade por integrante)
- Gestão de casos com TestLink (ao menos um cenário)
- Reporte de bugs em Git Issues
- Registro de uso de IA em `docs/ai/AI-LOG.md`

### Entrega 2 (peso 5)
- Testes unitários ampliados com isolamento de dependências
- Testes de integração
- Cobertura estrutural ≥ 80% (todas-arestas) com mutação ≥ 80%
- Testes de sistema com **Selenium**
- Inspeção de código (Sonar) e correção de defeitos
- Indicação de medidas da ISO 25010

> O uso de ferramentas de IA Generativa é permitido e incentivado, desde que documentado e avaliado criticamente em `docs/ai/AI-LOG.md`.

## Sobre o projeto — Banco Digital

Sistema web de banco digital em **Python + Flask** com login próprio e serviços bancários simulados. Foi desenhado para ser o alvo das técnicas de teste da disciplina: as regras de negócio ficam isoladas em classes puras (sem dependência do framework), cada uma com **complexidade ciclomática ≥ 10** — uma por integrante.

### Módulos de negócio (alvo dos testes)

| Módulo | Classe | Regras |
|---|---|---|
| PIX | `TransacaoPix` | validação de chaves, limites por horário/faixa, lista de bloqueio, chargeback |
| Juros | `CalculadoraJuros` | juros compostos, faixas de taxa por prazo, mora, aportes |
| Tarifas | `TarifaBancaria` | tarifa por tipo de conta, faixas de saldo, isenções, pacotes |
| Empréstimo | `SimuladorEmprestimo` | amortização Price/SAC, teto por renda, validações |
| Crédito | `DecisorCredito` | score por histórico, limites, aprovação/negação/parcial |

### Arquitetura

```
app/web  →  app/servicos  →  app/dominio
              │
              └── app/repositorios  →  SQLite / memória
```

- **`dominio/`** — regras de negócio puras (sem Flask), classe sob teste por integrante
- **`repositorios/`** — persistência com interface injetável (SQLite e memória) para isolamento nos testes
- **`servicos/`** — orquestração (autenticação, transferências)
- **`web/`** — blueprints e templates Jinja2 (login, dashboard, PIX, empréstimo, tarifas, crédito)

## Como executar

Requisito: [uv](https://docs.astral.sh/uv/) (gerencia a versão do Python e as dependências).

```bash
uv sync --all-extras            # cria o ambiente (Python 3.12) e instala as dependências
uv run flask --app app:create_app run
```

Acesse `http://127.0.0.1:5000` e crie uma conta em `/registro`.

A versão do Python é fixada em `.python-version` e as dependências em `pyproject.toml` (travadas em `uv.lock`).

## Qualidade e lint

```bash
uv run ruff check app/             # lint estático
uv run radon cc app/dominio -s     # complexidade ciclomática (CC ≥ 10 por módulo)
```

## Estrutura do Repositório

| Caminho | Descrição |
|---|---|
| `app/` | Código-fonte do sistema (Flask) |
| `app/dominio/` | Classes de negócio puras (alvo dos testes, CC ≥ 10) |
| `app/repositorios/` | Persistência (SQLite + memória) com interface injetável |
| `app/servicos/` | Orquestração (auth, transações) |
| `app/web/` | Rotas e telas (login, dashboard, PIX, empréstimo, tarifas, crédito) |
| `tests/unit/` | Testes unitários (1 arquivo por classe de domínio) |
| `docs/descricao_trabalho.md` | Enunciado do trabalho |
| `docs/plano_projeto.md` | Plano de projeto (stack, estrutura, roadmap das entregas) |
| `docs/aplicacao.md` | Documentação completa da aplicação e sua arquitetura |
| `docs/plano_de_teste.md` | Plano de Teste da Entrega 1 (escopo, ferramentas, artefatos, responsabilidades) |
| `docs/plano_de_teste_exemplo.md` | Exemplo preenchido de Plano de Teste (referência para preenchimento) |
| `tests/testes_manuais/` | Casos de teste manuais (Entrega 1) — PIX em [`tests/testes_manuais/pix/caso_pix.md`](tests/testes_manuais/pix/caso_pix.md) com evidências em `evidencias/` |
| `tests/testes_manuais/auth/` | Casos de teste manuais (Entrega 1) — Auth em [`tests/testes_manuais/auth/caso_auth.md`](tests/testes_manuais/auth/caso_auth.md) com evidências em `evidencias/` |
| `tests/testes_manuais/tarifas/` | Casos de teste manuais (Entrega 1) — Tarifas em [`tests/testes_manuais/tarifas/caso_tarifas.md`](tests/testes_manuais/tarifas/caso_tarifas.md) com evidências em `evidencias/` |
| `tests/testes_manuais/emprestimo/` | Casos de teste manuais (Entrega 1) — Empréstimo em [`tests/testes_manuais/emprestimo/caso_emprestimo.md`](tests/testes_manuais/emprestimo/caso_emprestimo.md) com evidências em `evidencias/` |
| `tests/testes_manuais/credito/` | Casos de teste manuais (Entrega 1) — Crédito em [`tests/testes_manuais/credito/caso_credito.md`](tests/testes_manuais/credito/caso_credito.md) com evidências em `evidencias/` |
| `docs/ai/AI-LOG.md` | Registro de uso de IA (a preencher nas entregas) |
| `docs/ai/prompts/sessao-11-caso-manual-tarifas.md` | [Sessão 11](docs/ai/prompts/sessao-11-caso-manual-tarifas.md) — Caso de teste manual de Tarifas |
| `pyproject.toml` | Dependências e configuração de ferramentas |
| `.python-version` | Versão do Python gerenciada pelo uv |

## Relatórios de TestLink

Os casos de teste manuais documentados no TestLink possuem relatórios em PDF exportados. O relatório do caso **Auth** (funcionalidade de autenticação) está disponível em:

📄 [Auth - Relatório TestLink (PDF)](https://drive.google.com/file/d/14yShZiduI8gixsV5wCQqA70DH2TV4SN4/view?usp=sharing)

## Contribuidores

- [alexandrelimaxs](https://github.com/alexandrelimaxs)
- [danielizu](https://github.com/danielizu)
- [pedro-mileipp](https://github.com/pedro-mileipp)
- [n2Gabrielle](https://github.com/n2Gabrielle)
- [ViniciusFelinto](https://github.com/ViniciusFelinto)
