# Plano de Projeto — Banco Digital

Documento de planejamento do Trabalho Prático da disciplina **Qualidade e Teste** (UFF 2026.2).

| Campo | Valor |
|---|---|
| Disciplina | Qualidade e Teste |
| Período | 2026.2 |
| Sistema | Banco Digital (web) |
| Stack | Python 3.12 (via uv) · Flask |
| Grupos | 5 integrantes |

---

## 1. Objetivo

Construir um sistema web de **banco digital** e aplicar, sobre ele, as técnicas de teste abordadas na disciplina: testes unitários, de integração e de sistema, cobertura estrutural, mutação, inspeção de código, ISO 25010 e testes manuais com gestão via TestLink. Todo o uso de ferramentas de IA Generativa será documentado em `docs/ai/AI-LOG.md`.

## 2. Decisões de stack

| Item | Decisão | Justificativa |
|---|---|---|
| Linguagem | Python 3.12 gerenciado via uv | Acessível, gratuito e leve para qualquer máquina; suporta todas as técnicas exigidas |
| Framework web | Flask + Jinja2 | Leve, simples de subir, server-rendered (sem SPA) — facilita testes de sistema com Selenium |
| Persistência | SQLite via repositórios injetáveis | Permite isolamento de dependências nos testes unitários (mock) e testes de integração realistas |
| Autenticação | Login/auth | Fornece um requisito não funcional (segurança) natural para a Entrega 2 e fluxos ricos no Selenium |
| Testes unitários | pytest | `parametrize`, fixtures, plugins |
| Isolamento | pytest-mock (`unittest.mock`) | Equivalente ao Mockito |
| Cobertura | coverage.py via pytest-cov (`branch = True`) | Equivalente ao JaCoCo para o critério todas-arestas |
| Mutação | mutmut | Equivalente ao PIT; escore ≥ 80% |
| Testes de sistema | Selenium WebDriver + webdriver-manager | Browser headless (Chrome/Chromium) |
| Medição de complexidade | radon (`radon cc`) | Justificar CC ≥ 10 das classes sob teste |
| Inspeção de código | ruff + SonarCloud | Lint local + inspeção com print para o relatório |
| CI | GitHub Actions | pytest + coverage + mutmut + ruff + SonarCloud automatizados |
| Bug tracking | GitHub Issues | Aceito pela regra "ou git issues" |
| Gestão de testes | TestLink | Ao menos 1 cenário; demais em planilha/documento |

## 3. Estrutura do repositório

```
.
├── app/
│   ├── __init__.py            # Factory do Flask (create_app)
│   ├── config.py              # Configurações (ambiente de teste, SQLite)
│   ├── dominio/               # Lógica pura — CLASSES SOB TESTE (CC >= 10, sem Flask)
│   │   ├── pix.py             # TransacaoPix
│   │   ├── juros.py           # CalculadoraJuros
│   │   ├── tarifas.py         # TarifaBancaria
│   │   ├── emprestimo.py      # SimuladorEmprestimo
│   │   └── credito.py         # DecisorCredito
│   ├── repositorios/          # Persistência (SQLite/in-memory) — interface injetável
│   │   ├── repositorio.py     # Protocol/ABC base
│   │   ├── sqlite_repositorio.py
│   │   └── memoria_repositorio.py   # usado em testes
│   ├── servicos/              # Orquestração domínio + repositório (auth, transferência...)
│   └── web/                   # Rotas Flask + templates (Jinja2)
│       ├── routes/
│       └── templates/
├── tests/
│   ├── unit/                  # 1 arquivo por classe de domínio
│   ├── integration/           # domínio ↔ repositório e fluxos web (test_client)
│   └── system/                # Selenium (requisitos funcionais)
├── docs/
│   ├── descricao_trabalho.md
│   ├── plano_projeto.md       # este documento
│   ├── plano_de_teste.md      # Entrega 1
│   ├── casos_manuais/         # planilha/documento de casos manuais (Entrega 1)
│   ├── relatorios/            # cobertura, mutação, ISO 25010, inspeção Sonar (Entrega 2)
│   └── ai/
│       └── AI-LOG.md          # registro de uso de IA
├── .github/workflows/ci.yml
├── .coveragerc
├── sonar-project.properties
├── pyproject.toml          # dependências (runtime e dev) + config de ferramentas
├── .python-version         # versão do Python gerenciada pelo uv
└── README.md                  # links para todos os artefatos
```

## 4. Módulos de domínio (uma classe por membro)

Requisito: cada classe deve ser **não-CRUD**, com **complexidade ciclomática ≥ 10** (desvios, laços e estruturas de controle). A divisão entre os integrantes será definida pelo grupo.

| Membro | Classe | Regras previstas |
|---|---|---|
| M1 | `TransacaoPix` | Validação de chave/valor; limites por horário e faixa; lista de bloqueio; chargeback |
| M2 | `CalculadoraJuros` | Juros compostos; faixas de taxa por período; juros de mora; arredondamento |
| M3 | `TarifaBancaria` | Tarifa por tipo de conta; faixas de saldo; isenções; pacotes de serviços |
| M4 | `SimuladorEmprestimo` | Parcelas Price vs SAC; teto por renda; taxa por prazo; inadimplência |
| M5 | `DecisorCredito` | Score por histórico; limites; aprovação/negação; laços sobre rendimentos |

Cada classe será projetada com `if/elif/for/while` suficientes para atingir CC ≥ 10, verificada por `radon cc` no CI.

## 5. Ferramentas de teste e integração contínua

### 5.1 Cobertura (todas-arestas)

- Configuração: `.coveragerc` com `branch = True`, `fail_under = 80` e exclusão de camadas web.
- Relatório por classe no CI; justificativa do mapeamento JaCoCo → coverage.py no relatório.

### 5.2 Mutação (mutmut)

- Execução sobre as mesmas classes do teste estrutural.
- Meta: escore de mutação ≥ 80%.
- Configuração de `tests_mutate` para as 5 classes de domínio.

### 5.3 Inspeção (Sonar)

- Projeto vinculado ao SonarCloud (gratuito para repositórios públicos).
- Print dos resultados (antes) e print após as correções de pelo menos uma classe por membro.

### 5.4 CI (GitHub Actions)

Jobs encadeados:
1. `lint` — ruff
2. `test` — pytest + pytest-cov (branch ≥ 80%)
3. `mutation` — mutmut (≥ 80%)
4. `complexity` — radon cc (assert CC ≥ 10 nas 5 classes)
5. `sonar` — scan do SonarCloud

## 6. Cronograma e entregas

### 6.1 Entrega 1 (Peso 3)

| # | Atividade | Artefato |
|---|---|---|
| 1 | Setup do repositório, estrutura e CI mínimo | código + `.github/workflows/ci.yml` |
| 2 | Implementação dos 5 módulos de domínio | `app/dominio/*.py` |
| 3 | Testes unitários (1 classe por membro) | `tests/unit/*` |
| 4 | Casos de teste manuais (1 funcionalidade por membro) | `docs/casos_manuais/` |
| 5 | Gestão de casos no TestLink (≥ 1 cenário) | capturas de tela + links |
| 6 | Plano de Teste (escopo, ferramentas, artefatos) | `docs/plano_de_teste.md` |
| 7 | Reporte de bugs | GitHub Issues |
| 8 | Registro de uso de IA | `docs/ai/AI-LOG.md` |

### 6.2 Entrega 2 (Peso 5)

| # | Atividade | Artefato |
|---|---|---|
| 1 | Ampliar unitários com isolamento de dependências (mock de repositórios) | `tests/unit/*` |
| 2 | Testes de integração (domínio ↔ repositório; fluxos web) | `tests/integration/*` |
| 3 | Cobertura estrutural ≥ 80% (todas-arestas) nas 5 classes | relatório + `docs/relatorios/` |
| 4 | Mutação ≥ 80% nas mesmas classes | relatório + `docs/relatorios/` |
| 5 | Testes de sistema (Selenium) com requisitos funcionais | `tests/system/*` |
| 6 | Inspeção Sonar + correção de 1 classe por membro (prints) | `docs/relatorios/inspecao_sonar.md` |
| 7 | ISO 25010: medidas por atributo com escala e justificativa | `docs/relatorios/iso25010.md` |
| 8 | NFR (segurança/desempenho) — opcional | testes específicos |

## 7. Requisitos do software (aderência ao enunciado)

### Obrigatório
- [ ] Código-fonte público no GitHub
- [ ] Classes com desvios, laços e estruturas de controle
- [ ] Pelo menos 5 classes (1 por membro) com CC ≥ 10
- [ ] Registro de IA em `docs/ai/AI-LOG.md`

### Desejável
- [x] Sistema web (Flask)
- Nota: o enunciado sugere Java para a classe de alta complexidade; como adotamos Python, será apresentada à professora a tabela de equivalência de ferramentas (Seção 2) para validação do nível de dificuldade e aderência.

## 8. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Mutação em Python menos "poderosa" que PIT → dificuldade de atingir 80% | Projetar regras densas (muitos branches); testes parametrizados fortes; monitorar escore no CI desde o início |
| Mapeamento JaCoCo → coverage.py questionado | Documentar equivalência no relatório de cobertura |
| CC ≥ 10 exigir esforço de projeto | Garantia via `radon cc` no CI; revisão do desenho das classes |
| SonarCloud config, token | Documentar setup; CI com secrets no repo público |

## 9. Referências

- Enunciado: `docs/descricao_trabalho.md`
- Template de Plano de Teste: apresentado em aula