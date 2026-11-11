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

## Testes e cobertura

```bash
uv run pytest                                             # toda a suíte
uv run pytest --cov --cov-branch --cov-report=term-missing # cobertura de arestas das 5 classes de domínio
uv run pytest tests/unit/test_credito.py --cov=app.dominio.credito --cov-branch --cov-report=term-missing
                                                          # cobertura de arestas de uma classe (ex.: DecisorCredito)
```

O relatório de cobertura do domínio lista as 5 classes; `skip_empty = True` ignora apenas arquivos sem código. Resultados por classe em [`docs/relatorios/cobertura_mutacao.md`](docs/relatorios/cobertura_mutacao.md).

### Testes de sistema (Selenium)

Pré-requisito: Google Chrome instalado (o driver é baixado automaticamente pelo Selenium Manager). Sem o Chrome, esses testes são pulados.

```bash
uv run pytest tests/system -v                 # roda os testes de sistema (Chrome headless)
EVIDENCIAS=1 uv run pytest tests/system       # salva prints de cada etapa em <funcionalidade>/evidencias/
```

Cada funcionalidade tem a sua pasta em `tests/system/` (ex.: `tests/system/credito/`), com os testes, o page object e as evidências. As fixtures compartilhadas (servidor Flask com banco temporário, navegador e cliente logado) estão em [`tests/system/conftest.py`](tests/system/conftest.py). Detalhes na seção 6.2 do [Plano de Teste](docs/plano_de_teste.md).

### Requisitos não funcionais

```bash
uv run pytest tests/rnf -v                    # todos os requisitos não funcionais, sem navegador
uv run pytest tests/rnf/seguranca -v          # só a segurança da autenticação (RNF06)
```

Cada requisito não funcional tem a sua pasta em `tests/rnf/` (ex.: `tests/rnf/seguranca/`). As fixtures compartilhadas (aplicação com banco temporário, cliente HTTP e cliente cadastrado) estão em [`tests/rnf/conftest.py`](tests/rnf/conftest.py).

Resultados e riscos identificados em [`docs/relatorios/rnf_seguranca.md`](docs/relatorios/rnf_seguranca.md). Detalhes na seção 6.3 do [Plano de Teste](docs/plano_de_teste.md).

## Inspeção com SonarQube local

O projeto usa o [SonarQube Community Build](https://www.sonarsource.com/products/sonarqube/) em Docker para a inspeção estática da Entrega 2. A análise inicial (“antes”) está documentada em [`docs/relatorios/inspecao_sonar.md`](docs/relatorios/inspecao_sonar.md), com prints e JSON em [`docs/relatorios/evidencias/sonar/antes/`](docs/relatorios/evidencias/sonar/antes/).

### Pré-requisitos

- Docker com Docker Compose;
- [uv](https://docs.astral.sh/uv/) para rodar a suíte e gerar o `coverage.xml`;
- `curl` e `jq`;
- `sonar-scanner` (opcional; se não estiver instalado, o script usa a imagem oficial `sonarsource/sonar-scanner-cli:latest` via Docker — a versão do scanner pode variar).

### Subir e analisar

```bash
# Sobe o SonarQube e aguarda o status UP
./scripts/sonar_local.sh up

# Gera o token local e associa o projeto ao perfil Python "Sonar way comprehensive"
./scripts/sonar_local.sh bootstrap

# Gera coverage.xml e envia a análise
./scripts/sonar_local.sh scan
```

O comando `scan` envia a análise mesmo que o `pytest` termine com falhas; o código de saída do pytest é preservado para não mascarar problemas. Na primeira execução, acesse `http://localhost:9000` com `admin` / `admin` e troque a senha. O token fica em `.sonar/token` (ignorado pelo Git) e não deve ser commitado. Se a senha do admin já tiver sido alterada, informe-a ao script:

```bash
SONAR_ADMIN_PASSWORD='sua-senha-local' ./scripts/sonar_local.sh bootstrap
```

### Comandos auxiliares

```bash
./scripts/sonar_local.sh status   # verifica se o SonarQube está UP
./scripts/sonar_local.sh token    # imprime o token atual
./scripts/sonar_local.sh down     # para o container, preservando os volumes
./scripts/sonar_local.sh reset    # remove container e volumes (apaga o histórico)
```

O container usa a imagem fixada `sonarqube:26.11.0.134175-community` e volumes nomeados (`sonarqube_data`, `sonarqube_extensions`, `sonarqube_logs`). A porta `9000` é publicada apenas para uso local; não exponha esse serviço na internet. O `sonar-project.properties` contém apenas configuração do projeto (sem token).

## Estrutura do Repositório

| Caminho | Descrição |
|---|---|
| `app/` | Código-fonte do sistema (Flask) |
| `app/dominio/` | Classes de negócio puras (alvo dos testes, CC ≥ 10) |
| `app/repositorios/` | Persistência (SQLite + memória) com interface injetável |
| `app/servicos/` | Orquestração (auth, transações) |
| `app/web/` | Rotas e telas (login, dashboard, PIX, empréstimo, tarifas, crédito) |
| `tests/unit/` | Testes unitários (1 arquivo por classe de domínio) |
| [`tests/system/`](tests/system/) | Entrega 2 — testes de sistema com Selenium: fixtures compartilhadas em `conftest.py` e uma pasta por funcionalidade |
| [`tests/system/credito/`](tests/system/credito/) | Testes de sistema — Crédito (RF06): [`test_credito_sistema.py`](tests/system/credito/test_credito_sistema.py), page object [`pagina_credito.py`](tests/system/credito/pagina_credito.py) e evidências em [`evidencias/`](tests/system/credito/evidencias/) |
| [`tests/rnf/`](tests/rnf/) | Entrega 2 — testes de requisitos não funcionais: fixtures compartilhadas em `conftest.py` e uma pasta por requisito |
| [`tests/rnf/seguranca/`](tests/rnf/seguranca/) | Segurança da autenticação (RNF06): [`test_seguranca_autenticacao.py`](tests/rnf/seguranca/test_seguranca_autenticacao.py) |
| [`docs/relatorios/rnf_seguranca.md`](docs/relatorios/rnf_seguranca.md) | Entrega 2 — relatório do RNF de segurança: verificações, riscos identificados e avaliação ISO 25010 (Segurança) |
| `docker-compose.yml` | SonarQube local com versão fixada e volumes persistentes |
| `scripts/sonar_local.sh` | Sobe o SonarQube, gera token e executa a análise |
| `sonar-project.properties` | Configuração do projeto para o SonarQube |
| `docs/relatorios/inspecao_sonar.md` | Relatório de inspeção com seções “antes” e “depois” |
| `docs/relatorios/evidencias/sonar/` | Prints e JSON das análises do SonarQube |
| `docs/descricao_trabalho.md` | Enunciado do trabalho |
| `docs/plano_projeto.md` | Plano de projeto (stack, estrutura, roadmap das entregas) |
| `docs/aplicacao.md` | Documentação completa da aplicação e sua arquitetura |
| `docs/plano_de_teste.md` | Plano de Teste da Entrega 1 (escopo, ferramentas, artefatos, responsabilidades) |
| `tests/testes_manuais/` | Casos de teste manuais (Entrega 1) — PIX em [`tests/testes_manuais/pix/caso_pix.md`](tests/testes_manuais/pix/caso_pix.md) com evidências em `evidencias/` |
| `tests/testes_manuais/auth/` | Casos de teste manuais (Entrega 1) — Auth em [`tests/testes_manuais/auth/caso_auth.md`](tests/testes_manuais/auth/caso_auth.md) com evidências em `evidencias/` |
| `tests/testes_manuais/tarifas/` | Casos de teste manuais (Entrega 1) — Tarifas em [`tests/testes_manuais/tarifas/caso_tarifas.md`](tests/testes_manuais/tarifas/caso_tarifas.md) com evidências em `evidencias/` |
| `tests/testes_manuais/emprestimo/` | Casos de teste manuais (Entrega 1) — Empréstimo em [`tests/testes_manuais/emprestimo/caso_emprestimo.md`](tests/testes_manuais/emprestimo/caso_emprestimo.md) com evidências em `evidencias/` |
| `tests/testes_manuais/credito/` | Casos de teste manuais (Entrega 1) — Crédito em [`tests/testes_manuais/credito/caso_credito.md`](tests/testes_manuais/credito/caso_credito.md) com evidências em `evidencias/` |
| `docs/ai/AI-LOG.md` | Registro de uso de IA (a preencher nas entregas) |
| `docs/ai/prompts/sessao-11-caso-manual-tarifas.md` | [Sessão 11](docs/ai/prompts/sessao-11-caso-manual-tarifas.md) — Caso de teste manual de Tarifas |
| `pyproject.toml` | Dependências e configuração de ferramentas |
| `.coveragerc` | Cobertura de arestas, caminhos relativos e gate de 80% |
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
