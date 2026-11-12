# Relatório de Cobertura Estrutural e Mutação — Entrega 2

Resultados das técnicas **estrutural** (critério todas-arestas, meta ≥ 80%) e **baseada em defeitos** (escore de mutação, meta ≥ 80%) por classe de domínio.

> As seções das demais classes são adicionadas pelos responsáveis de cada issue. A configuração padrão de cobertura e do mutmut é tratada na issue #36.

## Configuração do mutmut — #36

| Campo | Valor |
|---|---|
| Ferramenta | `mutmut` 3.8 (dev dependency) |
| Fonte mutada | `app/dominio` |
| Testes usados | `tests/unit` |
| Cache | `mutants/` (ignorado pelo Git) |
| Configuração | `[tool.mutmut]` em `pyproject.toml` |

```toml
[tool.mutmut]
source_paths = ["app/dominio"]
pytest_add_cli_args = ["-q"]
pytest_add_cli_args_test_selection = ["tests/unit"]
```

### Comandos

```bash
uv run mutmut run --max-children 8
uv run mutmut results
uv run mutmut show <id>
```

O `source_paths` explícito corrige o `FileNotFoundError` que o mutmut 3.8 apresentava sem configuração. A suíte unitária precisa estar 100% verde antes do run completo; as falhas abertas de PIX (#16/#17) e juros (#20) bloqueiam temporariamente o run geral.

Para mutar uma classe isolada, acrescente `only_mutate = ["app/dominio/<arquivo>.py"]` e restrinja `pytest_add_cli_args_test_selection` ao teste correspondente. Remova as duas restrições para o run completo de todas as classes.

### Validação piloto — `TarifaBancaria`

Para validar a configuração sem depender da suíte completa, foi executado um run piloto isolado em `app/dominio/tarifas.py` com `tests/unit/test_tarifas.py` (44 testes verdes), em um worktree temporário com `only_mutate` restrito à classe:

```text
106 mutantes gerados
74 mortos
32 sobreviventes
0 timeouts
0 suspeitos

Escore: 74 / 106 = 69,8%
```

**Resultado:** a configuração foi validada. O escore ainda está abaixo de 80%; a issue #45 (mutação de `TarifaBancaria`) deve adicionar testes para matar os 32 sobreviventes. A lista completa está em [`docs/relatorios/evidencias/mutacao/piloto-tarifas-resultados.txt`](evidencias/mutacao/piloto-tarifas-resultados.txt) e o resumo em [`piloto-tarifas.txt`](evidencias/mutacao/piloto-tarifas.txt).

> O run completo de todas as classes continua bloqueado pelas 3 falhas atuais da suíte (#16, #17 e #20).

---

## `DecisorCredito` — `app/dominio/credito.py`

| Campo | Valor |
|---|---|
| Responsável | Pedro Mileipp |
| Issues | #42 (unitários + cobertura estrutural) · #47 (mutação) |
| Arquivo de testes | `tests/unit/test_credito.py` |
| Complexidade ciclomática (soma dos métodos, `radon cc`) | 24 |

### Cobertura estrutural (todas-arestas) — #42

**Comando**

```bash
uv run pytest tests/unit/test_credito.py --cov=app.dominio.credito --cov-branch --cov-report=term-missing
```

**Antes × depois**

| | Antes (Entrega 1) | Depois (11/11/2026) |
|---|---|---|
| Casos de teste | 60 | 90 |
| Resultado | 55 passam · 5 falham | 90 passam |
| Cobertura de arestas | 93% | **100%** |
| Linhas não cobertas | 85, 92–94 | nenhuma |

**Saída (depois)**

```text
Name                     Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------
app/dominio/credito.py      71      0     40      0   100%
--------------------------------------------------------------------
TOTAL                       71      0     40      0   100%
90 passed
```

**Arestas que faltavam e os casos que passaram a cobri-las**

| Linha | Aresta | Casos (`TestDecidir::test_decidir_tabela_de_decisao`) |
|---|---|---|
| 85 | `score < 300` → `NEGADO` / `score_baixo` | `td_r1_score_0`, `td_r1_vl_score_299`, `td_r1_score_baixo_com_renda_alta` |
| 92–93 | `valor <= limite * 1.5` → `PARCIAL` | `td_r5_vl_valor_logo_acima_do_limite`, `td_r5_vl_valor_igual_1_5x_limite` |
| 94 | `valor > limite * 1.5` → `NEGADO` / `acima_limite` | `td_r6_vl_valor_logo_acima_de_1_5x`, `td_r6_score_alto_valor_muito_alto` |

Na Entrega 1, os testes de `decidir` usavam lista de histórico vazia (score 500), por isso nunca chegavam à regra de score baixo nem às faixas acima do limite.

### Técnicas funcionais aplicadas

A técnica de cada caso está no prefixo do id do `pytest.param`.

| Técnica | Prefixo | Casos | Onde |
|---|---|---|---|
| Partição de equivalência | `pe_` | 22 | um caso por tipo de evento do histórico; faixas de score; renda inválida |
| Análise de valor-limite | `vl_` | 33 | piso (0) e teto (1000) do score; fronteiras 299/300, 499/500, 699/700, 849/850; teto de limite de cada faixa (logo abaixo, no teto, logo acima) |
| Tabela de decisão | `td_` | 17 | as 6 regras de `decidir` e as combinações em que mais de uma regra se aplica |
| Teste de laços | `laco_` | 10 | 0, 1, 2, 3 e 100 iterações; clamp aplicado no meio do laço (a ordem dos eventos altera o resultado) |
| Parâmetros do construtor | `custom_` + 3 testes sem parâmetro | 8 | tetos com `base_limite=2000` e `limite_maximo=30000` |

> Na issue #47 foram acrescentados 6 casos `vl_` (piso e teto do score com passo 1: 999/1000/1001 e 1/0/-1), motivados pela análise de mutação. A suíte passou a ter **96 casos** (39 de valor-limite), mantendo 100% de cobertura de arestas.

**Tabela de decisão de `decidir`** (condições na ordem em que o código as avalia)

| Regra | C1 score < 300 | C2 limite == 0 | C3 valor ≤ 0 | C4 valor ≤ limite | C5 valor ≤ 1,5 × limite | Resultado |
|---|---|---|---|---|---|---|
| R1 | V | — | — | — | — | `NEGADO` / `score_baixo` |
| R2 | F | V | — | — | — | `NEGADO` / `sem_limite` |
| R3 | F | F | V | — | — | `NEGADO` / `valor_invalido` |
| R4 | F | F | F | V | — | `APROVADO` / `aprovado` |
| R5 | F | F | F | F | V | `PARCIAL` / `parcial` |
| R6 | F | F | F | F | F | `NEGADO` / `acima_limite` |

"—" indica condição irrelevante: a regra anterior já decidiu o resultado.

### Correções nos testes da Entrega 1

| Caso | Problema | Correção |
|---|---|---|
| `score_850`, `score_1000`, `fronteira_849_850` (renda 3000) | esperavam 5000; o correto é 2 × renda = 6000 | expectativa corrigida para 6000 |
| `teto_limite_max` (850, 20000) e (850, 50000) | esperavam 30000 usando o decisor padrão (teto 50000) | passaram a usar o `decisor_custom` (teto 30000), mantendo a intenção de testar o teto |
| `score_ok_valor_igual_limite` | o valor (1500) não era igual ao limite (3000) | valor ajustado para 3000 (`td_r4_vl_valor_igual_limite`) |
| `clamp_no_meio_do_laco`, `muitos_registros_loop` | um único registro, sem clamp e sem várias iterações | substituídos por casos reais de clamp no meio do laço e de 100 iterações |

Essas 5 falhas haviam sido reportadas no #35, fechado como erro de teste e não de código.

### Decisão de projeto: precedência das regras de `decidir`

A tabela de decisão mostrou combinações em que mais de uma regra se aplica, por exemplo score baixo **e** valor inválido. A especificação da classe (`docs/aplicacao.md`, seção 4.5) não define qual regra prevalece nesses casos.

Decisão adotada: manter a ordem de avaliação do código (score → limite → valor). Primeiro se avalia se o cliente pode receber crédito; só depois se avalia o pedido. Com isso:

| score | renda | valor | Resultado | Caso |
|---|---|---|---|---|
| 299 | 3000 | -1 | `NEGADO` / `score_baixo` | `td_r1_precedencia_sobre_valor_negativo` |
| 500 | 0 | 0 | `NEGADO` / `sem_limite` | `td_r2_precedencia_sobre_valor_zero` |

Nos dois casos o pedido é negado; o que muda é só o motivo informado. Os casos acima fixam esse comportamento na suíte, de modo que uma mudança na ordem das regras é detectada pelos testes.

### Mutação (baseada em defeitos) — #47

**Ferramenta:** mutmut 3.8.0, com a configuração `[tool.mutmut]` da issue #36 (`source_paths = ["app/dominio"]`).

A suíte unitária completa ainda tem 3 falhas (bugs #16, #17 e #20, de outras classes), e o mutmut só roda com a suíte selecionada toda passando. Por isso foi usada a receita de **classe isolada** da issue #36: acrescentar temporariamente ao `pyproject.toml`, sem versionar,

```toml
only_mutate = ["app/dominio/credito.py"]
pytest_add_cli_args_test_selection = ["tests/unit/test_credito.py"]
```

**Comandos**

```bash
uv run mutmut run --max-children 4
uv run mutmut results
uv run mutmut show <mutante>
```

**Resultado (12/11/2026)**

| | 1ª execução — antes (suíte da #42, 90 casos) | 2ª execução — depois (suíte da #47, 96 casos) |
|---|---|---|
| Mutantes gerados | 184 | 184 |
| Mortos | 178 | **179** |
| Sobreviventes | 6 | 5 (todos equivalentes) |
| Timeout / suspeitos | 0 | 0 |
| Escore (mortos / gerados) | 96,7% | **97,3%** |
| Escore descontando os equivalentes (mortos / não equivalentes) | 178 / 179 = 99,4% | **179 / 179 = 100%** |
| Evidência | [`credito-execucao-1-antes.txt`](evidencias/mutacao/credito-execucao-1-antes.txt) | [`credito-execucao-2-depois.txt`](evidencias/mutacao/credito-execucao-2-depois.txt) |

Meta da disciplina: ≥ 80%. ✅

Cada arquivo de evidência traz a configuração, o comando, o resumo, o diff de cada sobrevivente e a lista completa dos 184 mutantes.

**Análise dos sobreviventes da 1ª execução**

| Mutante | Linha original → mutação | Classificação | Justificativa |
|---|---|---|---|
| `calcular_score__mutmut_50` | `if score < 0:` → `if score <= 0:` | Equivalente | Com `score == 0`, o mutante executa `score = 0`, que não muda nada |
| `calcular_score__mutmut_51` | `if score < 0:` → `if score < 1:` | Equivalente | O score é inteiro (`peso: int`); o único valor afetado é 0, que é atribuído como 0 |
| `calcular_score__mutmut_54` | `if score > 1000:` → `if score >= 1000:` | Equivalente | Com `score == 1000`, o mutante executa `score = 1000`, que não muda nada |
| `calcular_score__mutmut_55` | `if score > 1000:` → `if score > 1001:` | **Morto na 2ª execução** | Nenhum caso chegava a exatamente 1001: "adiantamento" soma de 2 em 2 (de 500 vai a 1000 ou 1002). O caso `vl_score_1001_vira_1000` (`pagamento_em_dia`, peso 501) mata o mutante |
| `limite_por_score__mutmut_1` | `if renda <= 0:` → `if renda < 0:` | Equivalente | Com renda 0, todas as faixas seguintes devolvem `min(0 × fator, teto) = 0` (os tetos são positivos), mesmo resultado do `return 0.0` |
| `limite_por_score__mutmut_23` | `min(renda * 1.0, …)` → `min(renda / 1.0, …)` | Equivalente | Multiplicar e dividir por 1 dão o mesmo valor |

Três dos equivalentes estão nos `if` de clamp do score (piso 0 e teto 1000). Essas comparações existem para manter a complexidade ciclomática da classe ≥ 10, requisito da disciplina; reescrevê-las com `max`/`min` eliminaria os mutantes, mas também reduziria a CC.

**Lição registrada:** a cobertura de arestas já era de 100%, mas a mutação mostrou uma fronteira não testada (score 1001). Cobertura completa não garante que os valores-limite foram exercitados.
