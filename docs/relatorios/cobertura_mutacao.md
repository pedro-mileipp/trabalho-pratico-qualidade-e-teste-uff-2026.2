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

O `source_paths` explícito corrige o `FileNotFoundError` que o mutmut 3.8 apresentava sem configuração. A suíte unitária precisa estar 100% verde antes do run completo. Desde 22/11/2026 a suíte está verde — os bugs #16, #17 e #20 foram corrigidos — e os 3 `xfail` restantes (defeito #78) não bloqueiam o mutmut.

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

> **Atualização (#45, 22/11/2026):** com a suíte ampliada na #40 e na #45, o escore de `TarifaBancaria` chegou a **94,3%** (100% descontando 6 equivalentes). Ver a subseção "Mutação — #45" na seção da classe.

> O run completo de todas as classes pode ser executado: a suíte está verde desde 22/11/2026 (os bugs #16, #17 e #20 foram corrigidos; restam 3 `xfail` do defeito #78).

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

---

## `CalculadoraJuros` — `app/dominio/juros.py`

| Campo | Valor |
|---|---|
| Responsável | Gabrielle Rosa (`n2Gabrielle`) |
| Issues | #39 (unitários ampliados + cobertura estrutural todas-arestas) · #20 (correção prévia do desconto de IR no mês 12) |
| Arquivo de testes | `tests/unit/test_juros.py` |

### Cobertura estrutural (todas-arestas) — #39

**Comando**

```bash
.venv/bin/pytest tests/unit/test_juros.py --cov=app.dominio.juros --cov-branch --cov-report=term-missing -v
```

**Antes × depois**

| Métrica | Antes (Entrega 1 / #20) | Depois (20/11/2026 — #39) |
|---|---|---|
| Casos de teste | 36 | 68 |
| Resultado | 36 passam | 68 passam (0.50s) |
| Cobertura de linhas e ramos | 100% | **100.00%** |
| Linhas / ramos não cobertos | nenhuma (67 stmts, 36 branches) | nenhuma (67 stmts, 0 miss, 36 branches, 0 partial) |

**Saída (20/11/2026)**

```text
Name                   Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------
app/dominio/juros.py      67      0     36      0   100%
------------------------------------------------------------------
TOTAL                     67      0     36      0   100%
Required test coverage of 80.0% reached. Total coverage: 100.00%
68 passed in 0.50s
```

### Técnicas aplicadas

A técnica de cada caso está identificada pelo prefixo do `pytest.param` ou por comentário em `tests/unit/test_juros.py`.

| Técnica | Prefixo | Cobertura nos casos adicionados |
|---|---|---|
| Partição de equivalência | `pe_` | Prazos por faixa (`pe_prazo_*`) e cenários de atraso em `total_a_pagar` (`pe_total_*`) |
| Análise de valor-limite | `vl_` | Prazos negativo/zero (`vl_prazo_*`), fronteiras de dias de atraso 15/16 e 60/61 (`vl_total_mora_limite_*`) e trava de R$ 1.000.000,00 no laço de aportes (`test_montante_com_aportes_vl_trava_um_milhao_estrita`) |
| Tabela de decisão | `td_` | Combinações de capitalização de aporte, incidência de IR no mês 12 e patamar acima/abaixo de R$ 1.000.000,00 (`td_r1_*` a `td_r6_*`) |
| Teste de laços | `laco_` | Variações de iterações em `calcular_montante` (1, 3, 13, 24 e 36 meses) e ciclos de IR em `montante_com_aportes` (1, 6, 13, 18 e 24 meses) |

### Observações e validação

As 16 falhas iniciais nos novos casos vieram de expectativas ou parâmetros incorretos nos testes:

- mora sobre o montante composto em `total_a_pagar`;
- capitalização mensal por iteração no laço de `montante_com_aportes`;
- taxa por faixa em `calcular_montante`;
- `taxa_anual=0.12` para exercitar a trava de R$ 1.000.000,00 no laço.

Esses problemas não eram defeitos no código de produção. Após o ajuste das expectativas e parâmetros, todos os 68 casos passaram, mantendo 100.00% de cobertura estrutural, sem alterar `app/dominio/juros.py`.


### Mutação (baseada em defeitos) — #44

**Ferramenta:** `.venv/bin/mutmut`, com configuração isolada temporária em `[tool.mutmut]`:

```toml
only_mutate = ["app/dominio/juros.py"]
pytest_add_cli_args_test_selection = ["tests/unit/test_juros.py"]
```

A configuração temporária foi revertida após a medição.

**Comandos**

```bash
.venv/bin/mutmut run --max-children 4
.venv/bin/mutmut results
```

**Resultado (20/11/2026)**

| Métrica | Valor |
|---|---:|
| Mutantes gerados | 149 |
| Mutantes mortos | 130 |
| Mutantes sobreviventes | 19 |
| Timeout / suspeitos / ignorados | 0 |
| Escore (mortos / gerados) | **87,25%** |

**Meta da disciplina:** ≥ 80%. ✅

**Evidência:** [`juros-mutacao.txt`](evidencias/mutacao/juros-mutacao.txt)

### Lista dos sobreviventes

| Mutante | Classificação |
|---|---|
| `CalculadoraJuros.__init__.__mutmut_12` | Equivalente |
| `CalculadoraJuros.taxa_mensal__mutmut_1` | Equivalente |
| `CalculadoraJuros.calcular_montante__mutmut_1` | Equivalente |
| `CalculadoraJuros.calcular_montante__mutmut_2` | Sem novo caso nesta etapa |
| `CalculadoraJuros.calcular_montante__mutmut_4` | Equivalente |
| `CalculadoraJuros.juros_de_mora__mutmut_1` | Equivalente |
| `CalculadoraJuros.juros_de_mora__mutmut_2` | Sem novo caso nesta etapa |
| `CalculadoraJuros.total_a_pagar__mutmut_1` | Sem novo caso nesta etapa |
| `CalculadoraJuros.montante_com_aportes__mutmut_1` | Sem novo caso nesta etapa |
| `CalculadoraJuros.montante_com_aportes__mutmut_2` | Sem novo caso nesta etapa |
| `CalculadoraJuros.montante_com_aportes__mutmut_4` | Sem novo caso nesta etapa |
| `CalculadoraJuros.montante_com_aportes__mutmut_6` | Equivalente |
| `CalculadoraJuros.montante_com_aportes__mutmut_12` | Equivalente |
| `CalculadoraJuros.montante_com_aportes__mutmut_39` | Equivalente |
| `CalculadoraJuros.montante_com_aportes__mutmut_45` | Equivalente |
| `CalculadoraJuros.montante_com_aportes__mutmut_46` | Equivalente |
| `CalculadoraJuros.montante_com_aportes__mutmut_47` | Equivalente |
| `CalculadoraJuros.montante_com_aportes__mutmut_51` | Sem novo caso nesta etapa |
| `CalculadoraJuros.montante_com_aportes__mutmut_52` | Sem novo caso nesta etapa |

### Justificativa dos equivalentes

- `__init__.__mutmut_12`: a faixa final `(37, 0.30)` mantém o comportamento padrão para valores acima do limite.
- `taxa_mensal__mutmut_1`: a mutação troca `taxa_anual < 0` por `taxa_anual <= 0`; com `taxa_anual == 0.0`, o resultado continua sendo `0.0`.
- `calcular_montante__mutmut_1`: a mutação troca `principal < 0` por `principal <= 0`; com `principal == 0`, o resultado permanece `0.0`.
- `calcular_montante__mutmut_4` e `montante_com_aportes__mutmut_6`: a mutação troca `meses < 0` por `meses <= 0`; com `meses == 0`, o laço não executa e o resultado continua sendo o principal arredondado.
- `juros_de_mora__mutmut_1`: a mutação troca `valor < 0` por `valor <= 0`; com `valor == 0`, multa e juros continuam sendo `0.0`.
- `montante_com_aportes__mutmut_12`: a mutação troca `taxa_anual < 0` por `taxa_anual <= 0`; com taxa zero, o laço soma o aporte mensal sem IR ou trava, mantendo o mesmo resultado.
- `montante_com_aportes__mutmut_39`: a mutação troca `aliquota_ir >= 0` por `aliquota_ir > 0`; com alíquota zero, subtrair `0.0` não altera o resultado.
- `montante_com_aportes__mutmut_45` e `montante_com_aportes__mutmut_46`: os limites alterados (`mes >= 0` e `mes > 1` em vez de `mes > 0`) não mudam o resultado dentro de `range(1, meses + 1)`, incluindo o desconto no mês 12.
- `montante_com_aportes__mutmut_47`: nos cenários atuais, com `aliquota_ir = 0.15`, a comparação continua satisfeita tanto pela subtração do IR quanto pela atribuição direta.

### Decisão

Como a suíte alcançou **87,25% de mutação**, acima da meta de 80%, e **100% de cobertura estrutural**, optou-se por não adicionar novos casos de teste nesta etapa. Os oito sobreviventes não classificados como equivalentes permaneceram documentados na evidência para análise futura.

---

## `SimuladorEmprestimo` — `app/dominio/emprestimo.py`

| Campo | Valor |
|---|---|
| Responsável | Vinicius Sales Felinto |
| Issues | #41 (unitários + cobertura estrutural todas-arestas) · #46 (mutação) |
| Arquivo de testes | `tests/unit/test_emprestimo.py` |
| Complexidade ciclomática (soma dos métodos, `radon cc`) | 26 |

### Cobertura estrutural (todas-arestas) — #41

**Comando**

```bash
uv run pytest tests/unit/test_emprestimo.py --cov=app.dominio.emprestimo --cov-branch --cov-report=term-missing
```

**Antes × depois**

| Métrica | Antes (Entrega 1) | Depois (22/11/2026 — #41) |
|---|---|---|
| Casos de teste | 40 | 118 |
| Resultado | 40 passam | 118 passam |
| Cobertura de linhas e ramos | 100% | **100%** |
| Linhas / ramos não cobertos | nenhuma (82 stmts, 38 branches) | nenhuma (82 stmts, 0 miss, 38 branches, 0 partial) |

**Saída (22/11/2026)**

```text
Name                        Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------
app/dominio/emprestimo.py      82      0     38      0   100%
-----------------------------------------------------------------------
TOTAL                          82      0     38      0   100%
Required test coverage of 80.0% reached. Total coverage: 100.00%
118 passed in 0.88s
```

### Técnicas aplicadas

A técnica de cada caso está identificada pelo prefixo do id do `pytest.param` ou pelo nome do teste em `tests/unit/test_emprestimo.py`.

| Técnica | Prefixo | Casos | Onde |
|---|---|---|---|
| Partição de equivalência | `pe_` | 26 | Faixas de prazo em `taxa_por_prazo`; faixas salariais em `teto_por_renda`; taxa zero e prazos em `parcelas_price`/`sac`; classes de entradas válidas/inválidas de `simular` |
| Análise de valor-limite | `vl_` | 52 | Fronteiras de prazos (0, 1, 2, 5, 6, 7, 11, 12, 13, 35, 36, 37, 60); fronteiras de renda (-0.01, 0.0, 0.01, 1999.99, 2000.0, 2000.01, 4999.99, 5000.0, 5000.01, 9999.99, 10000.0, 10000.01); fronteiras de entrada de `simular` (principal 0, 0.01, 99.99, 100; meses 0, 1, 2, 60, 61; score 398, 399, 400, 401, 1000); fronteiras exatas de teto por renda (no teto e logo acima) e comprometimento de renda |
| Tabela de decisão | `td_` | 24 | As 11 regras canônicas de `simular` (R1 a R11) e todas as combinações de conflito/precedência entre validações simultâneas |
| Teste de laços | `laco_` | 8 | Variações de iterações em `parcelas_sac`: 0 (divisão por zero), 1, 2 (piso), 4 e 12 (n típico), 59 (max-1), 60 (max) e 61 (max+1) |
| Parâmetros do construtor | `custom_` | 4 | Configurações personalizadas de `taxa_base`, `valor_minimo`, `prazo_min`, `prazo_max` e `teto_comprometimento` |
| Conferência numérica completa | — | 4 | Conferência estrita de cada parcela individual, número de parcelas e total acumulado para amortizações Price e SAC |

**Tabela de decisão de `simular`** (condições na ordem em que o código as avalia)

| Regra | C1 P ≤ 0 | C2 P < min | C3 M < min | C4 M > max | C5 R ≤ 0 | C6 Inadimplente | C7 Score < 400 | C8 P > Teto | C9 Parcela > Comp | Sistema | Resultado | Motivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 | V | — | — | — | — | — | — | — | — | — | NEGADO | `valor_invalido` |
| R2 | F | V | — | — | — | — | — | — | — | — | NEGADO | `valor_abaixo_minimo` |
| R3 | F | F | V | — | — | — | — | — | — | — | NEGADO | `prazo_curto` |
| R4 | F | F | F | V | — | — | — | — | — | — | NEGADO | `prazo_longo` |
| R5 | F | F | F | F | V | — | — | — | — | — | NEGADO | `renda_invalida` |
| R6 | F | F | F | F | F | V | — | — | — | — | NEGADO | `inadimplente` |
| R7 | F | F | F | F | F | F | V | — | — | — | NEGADO | `score_baixo` |
| R8 | F | F | F | F | F | F | F | V | — | — | NEGADO | `acima_teto` |
| R9 | F | F | F | F | F | F | F | F | V | — | NEGADO | `comprometimento_acima` |
| R10 | F | F | F | F | F | F | F | F | F | PRICE | APROVADO | `aprovado` |
| R11 | F | F | F | F | F | F | F | F | F | SAC | APROVADO | `aprovado` |

"—" indica condição irrelevante (curto-circuito pela regra anterior).

### Decisão de projeto: precedência e avaliação estrita de parcelas

1. **Precedência de validação:** O método `simular()` avalia as restrições em pipeline estrito: primeiro o valor do empréstimo (positivo e acima do mínimo), depois os prazos, em seguida a renda e o cliente (inadimplência e score), depois a capacidade patrimonial (`principal > teto_por_renda`) e, por fim, o comprometimento da primeira parcela. Foram adicionados 13 casos de teste exercitando combinações onde múltiplos critérios falham simultaneamente, garantindo a estabilidade da interface e o motivo retornado.
2. **Cálculos numéricos e mutação:** Para mitigar mutantes aritméticos gerados em cálculos financeiros (como alterações nos operadores de amortização, fator exponencial de juros ou cálculo do total pago), os testes não se limitam a checar `aprovado == True`. Cada caso aprovado valida:
   - `valor_parcela` exato com arredondamento a duas casas decimais;
   - `numero_parcelas` correspondente;
   - `parcelas` (lista completa com cada valor periódico);
   - `total_pago` igual à soma exata das parcelas arredondadas.
3. **Ausência de defeitos no código de produção:** Todos os 118 casos foram validados e passaram com 100% de sucesso. Não foram detectados bugs em `app/dominio/emprestimo.py`, cuja lógica atende com fidelidade às especificações de domínio. Nenhuma issue de bug corretivo precisou ser aberta para a classe.

### Mutação (baseada em defeitos) — #46

**Ferramenta:** `mutmut` 3.8.0 engine (trampoline / AST / `libcst`), com isolamento de classe configurado em `[tool.mutmut]`:

```toml
only_mutate = ["app/dominio/emprestimo.py"]
source_paths = ["app/dominio"]
pytest_add_cli_args = ["-q"]
pytest_add_cli_args_test_selection = ["tests/unit/test_emprestimo.py"]
---

## `TarifaBancaria` — `app/dominio/tarifas.py`

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielcamposs`) |
| Issues | #40 (unitários + cobertura estrutural) · #45 (mutação) |
| Arquivo de testes | `tests/unit/test_tarifas.py` |
| Complexidade ciclomática (`radon cc`) | `tarifa_mensal` = 12; soma dos métodos da classe = 24 |

### Cobertura estrutural (todas-arestas) — #40

**Comando**

```bash
uv run pytest tests/unit/test_tarifas.py --cov=app.dominio.tarifas --cov-branch --cov-report=term-missing
```

**Antes × depois**

| | Antes (Entrega 1) | Depois (22/11/2026) |
|---|---|---|
| Casos de teste | 44 | 122 |
| Resultado | 44 passam | 118 passam · 4 `xfail` (defeitos #77 e #78) |
| Cobertura de arestas | 97% | **100%** |
| Linhas não cobertas | 49 | nenhuma |

**Saída (depois)**

```text
Name                     Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------
app\dominio\tarifas.py      54      0     24      0   100%
--------------------------------------------------------------------
TOTAL                       54      0     24      0   100%
118 passed, 4 xfailed
```

Evidências em [`evidencias/cobertura/`](evidencias/cobertura/): [`tarifas-4-prompt-tecnico-final.txt`](evidencias/cobertura/tarifas-4-prompt-tecnico-final.txt) (versão final) e [`tarifas-defeitos-runxfail.txt`](evidencias/cobertura/tarifas-defeitos-runxfail.txt) (falha real dos defeitos). As versões intermediárias geradas pela IA estão nos arquivos `tarifas-1` a `tarifas-3` (ver "Revisão da solução gerada por IA").

**Arestas que faltavam e os casos que passaram a cobri-las**

| Linha | Aresta | Casos |
|---|---|---|
| 48 → 49 | sem pacote, sem isenção, `antiguidade_meses >= 36` → desconto de 20% | `vl_antiguidade_36_com_desconto`, `vl_antiguidade_37_com_desconto`, `vl_premium_antiguidade_36`, `pe_corrente_antiguidade_alta`, `td_sp_07`, `td_sp_08`, `td_sp_11`, `td_sp_12`, `td_sp_premium_*` |
| 40 (condição) | com pacote, `antiguidade_meses >= 24` → meia tarifa | `vl_pacote_antiguidade_23/24/25`, `td_cp_corrente_1000_antig_24`, `td_cp_pacote_ignora_transacoes` |

A condição da linha 40 não aparecia como faltando porque o `coverage` mede arestas, não condições: a aresta já era coberta pela parte `saldo >= 5000`. Mesmo assim, nenhum teste exercitava a parte da antiguidade, que foi incluída para completar a tabela de decisão.

Na Entrega 1, os casos de antiguidade tinham sido removidos porque a rota web não expõe `antiguidade_meses`.

### Técnicas funcionais aplicadas

A técnica de cada caso novo está no prefixo do id do `pytest.param`. Os 44 casos da Entrega 1 foram mantidos como estavam (apenas o id `premium_pacote_isencao_5x5` foi renomeado para `premium_pacote_isento_saldo_limite_50000`).

| Técnica | Prefixo | Casos novos | Onde |
|---|---|---|---|
| Partição de equivalência | `pe_` | 21 | as 18 combinações de tipo de conta × pacote × saldo (negativo / zero / positivo), completando as da Entrega 1; antiguidade negativa (inválida), nova, média e alta; `tarifa_anual` com valores explícitos |
| Análise de valor-limite | `vl_` | 25 | faixas de isenção 999,99/1000, 4999,99/5000/5000,01, 49999,99/50000; antiguidade 35/36/37 (sem pacote) e 23/24/25 (com pacote); saldo -0,01/0; transações 9/10/11 combinadas com o desconto; `_tem_isencao` nas fronteiras |
| Tabela de decisão | `td_` | 29 | tabela sem pacote (12 combinações + 3 na premium), tabela com pacote (11 casos) e 3 casos da premium na regra R3, que revelaram o defeito #78 |
| Parâmetros personalizados | `custom_` | 2 | desconto por antiguidade e sobretaxa com `TarifasBase` alterada |
| Defeito (sem prefixo) | — | 1 | `test_defeito_tarifa_anual_aplica_desconto_por_antiguidade` (#77) |
| Teste de laços | — | 0 | **Não se aplica:** `TarifaBancaria` não possui laços |

**Tabela de decisão 1 — `tarifa_mensal` sem pacote** (conta corrente, base 30,00; 12 transações = +5,00 de extras)

C1 (saldo ≥ 5000) e C3 (saldo < 0) não podem ser verdadeiras juntas, por isso há 12 combinações possíveis, e não 16. A precedência do `if/elif` é isenção > antiguidade > saldo negativo; as extras somam em todas.

| Caso | C1 isenção | C2 antig. ≥ 36 | C3 saldo < 0 | C4 extras | Resultado |
|---|---|---|---|---|---|
| `td_sp_01` | V | F | F | F | 0,00 |
| `td_sp_02` | V | F | F | V | 5,00 |
| `td_sp_03` | V | V | F | F | 0,00 |
| `td_sp_04` | V | V | F | V | 5,00 |
| `td_sp_05` | F | F | F | F | 30,00 |
| `td_sp_06` | F | F | F | V | 35,00 |
| `td_sp_07` | F | V | F | F | 24,00 |
| `td_sp_08` | F | V | F | V | 29,00 |
| `td_sp_09` | F | F | V | F | 36,00 |
| `td_sp_10` | F | F | V | V | 41,00 |
| `td_sp_11` | F | V | V | F | 24,00 |
| `td_sp_12` | F | V | V | V | 29,00 |

Na premium (base 50,00, isenção a partir de 50000) foram acrescentadas 3 linhas: `td_sp_premium_isento_limite_com_antiguidade` (0,00), `td_sp_premium_antiguidade_prevalece_negativo` (40,00) e `td_sp_premium_antiguidade_extras` (52,50). Algumas linhas coincidem com casos `vl_` ou da Entrega 1; elas foram mantidas para que a tabela fique completa sozinha.

**Tabela de decisão 2 — `tarifa_mensal` com pacote** (tipo × saldo ≥ 50000 × saldo ≥ 5000 × antiguidade ≥ 24)

Como saldo ≥ 50000 implica saldo ≥ 5000, há 3 faixas de saldo (1000 / 20000 / 60000). São 2 tipos × 3 faixas × 2 antiguidades = 12 combinações. A poupança decide antes (R1, `td_cp_r1_poupanca_prevalece_sobre_tudo`: 0,00).

| Tipo | Saldo | Antig. 0 | Antig. 24 |
|---|---|---|---|
| corrente | 1000 | 30,00 | 15,00 |
| corrente | 20000 | 15,00 | 15,00 |
| corrente | 60000 | 15,00 | 15,00 |
| premium | 1000 | 35,00 | 15,00 → esperado 25,00 (**#78**) |
| premium | 20000 | 15,00 → esperado 25,00 (**#78**) | 15,00 → esperado 25,00 (**#78**) |
| premium | 60000 | 0,00 | 0,00 |

Com pacote, as transações extras são ignoradas (`td_cp_pacote_ignora_transacoes`) e não há sobretaxa de saldo negativo (`pe_corrente_pacote_saldo_negativo`: 30,00).

**Precedências fixadas** (a especificação não as define; o comportamento atual foi mantido e documentado):

| Combinação | Resultado | Caso |
|---|---|---|
| poupança com pacote, saldo negativo, 20 transações, 40 meses | 0,00 | `td_cp_r1_poupanca_prevalece_sobre_tudo` |
| corrente com saldo 6000 e 36 meses | 0,00 (isenção prevalece sobre o desconto) | `td_sp_03_isento_antiguidade` |
| corrente com saldo negativo e 36 meses | 24,00 (desconto prevalece; a sobretaxa não é cobrada) | `td_sp_11_antiguidade_prevalece_negativo` |
| premium com pacote, saldo 60000 e 24 meses | 0,00 (isenção total prevalece sobre a meia tarifa) | `td_cp_premium_60000_isento_prevalece_antiguidade` |

### Defeitos revelados

| Issue | Defeito | Esperado × atual | Caso |
|---|---|---|---|
| [#77](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/77) | `tarifa_anual` não recebe nem repassa `antiguidade_meses` | 288,00 × `TypeError` (sempre 360,00) | `test_defeito_tarifa_anual_aplica_desconto_por_antiguidade` |
| [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78) | meia tarifa do pacote premium usa a tarifa da corrente (suspeito, a confirmar pelo grupo) | 25,00 × 15,00 | `test_defeito_pacote_premium_meia_tarifa_da_premium[td_r3_*]` (3 casos) |

Os casos afirmam o comportamento esperado e estão marcados com `@pytest.mark.xfail(strict=True)`, para a suíte continuar verde e não bloquear o mutmut (#45). O caso do #77 usa `raises=TypeError`, para que só a falha do defeito seja aceita. Ao corrigir, o `xfail` deve ser removido (com `strict=True`, o pytest acusa XPASS).

**Outras observações (sem issue de bug):**

- `_tarifa_com_pacote` (linhas 54–59) **nunca é chamado** por `tarifa_mensal`, que reimplementa a regra do pacote de forma diferente. É código morto; fica como entrada para a #50 (Sonar). Os testes da Entrega 1 sobre esse método foram mantidos.
- A faixa de isenção da poupança (`faixas_isencao[0]` = 1000) **nunca é consultada por `tarifa_mensal`**, que devolve 0 para a poupança antes de verificar a isenção (`vl_poupanca_mensal_999_99` e `vl_poupanca_mensal_1000` dão 0,00). A linha 66 de `_tem_isencao` só é coberta porque os testes chamam o método privado diretamente. Também é entrada para a #50.
- `antiguidade_meses` negativa não é validada e é tratada como conta nova (`pe_antiguidade_negativa_sem_validacao`). A especificação não define validação; o comportamento ficou fixado no teste.

### Revisão da solução gerada por IA

Os casos foram gerados com apoio do Claude Code ([sessão 20 do AI-LOG](../ai/prompts/sessao-20-cobertura-tarifas.md)) em duas rodadas. Cada rodada teve a solução da IA gravada sem revisão e depois revisada:

| Rodada | Solução inicial (IA) | Solução final (revisada) |
|---|---|---|
| 1 — plano da issue | `70ccd5c`: 95 passed, 3 xfailed ([`tarifas-1`](evidencias/cobertura/tarifas-1-solucao-inicial.txt)) | `ee613a6`: 94 passed, 3 xfailed ([`tarifas-2`](evidencias/cobertura/tarifas-2-solucao-final.txt)) |
| 2 — prompt técnico do responsável | `eaafc09`: 115 passed, 4 xfailed ([`tarifas-3`](evidencias/cobertura/tarifas-3-prompt-tecnico-inicial.txt)) | `3809dcc`: 118 passed, 4 xfailed ([`tarifas-4`](evidencias/cobertura/tarifas-4-prompt-tecnico-final.txt)) |

As duas soluções iniciais já tinham 100% de cobertura de arestas. Os problemas abaixo **não apareciam na execução**:

| Rodada | Problema na solução inicial | Como foi identificado | Correção |
|---|---|---|---|
| 1 | 2 casos `pe_` duplicados | comparação dos parâmetros | removidos |
| 1 | faltava a partição inválida (antiguidade negativa) | revisão das classes de equivalência | `pe_antiguidade_negativa_sem_validacao` |
| 1 | `tarifa_anual` testada com oráculo calculado pelo próprio código | mutação manual temporária (`corrente * 0.5` → `0.6`): o teste inicial **continuou passando**, o final falhou ([evidência](evidencias/cobertura/tarifas-verificacao-oraculo-anual.txt)) | valores esperados explícitos |
| 1 | `xfail` do #77 aceitava qualquer exceção | saída com `--runxfail` (a falha real era `TypeError`) | `raises=TypeError` |
| 2 | ao substituir a tabela de decisão antiga, 3 cenários da premium sem pacote foram perdidos (isenção no limite 50000 com antiguidade, antiguidade com saldo negativo, antiguidade com extras) | comparação dos casos removidos com os novos | tabela sem pacote passou a receber o tipo, com 3 linhas `td_sp_premium_*` |
| 2 | o relatório e o plano citavam ids que deixaram de existir (`td_r1_*`, `td_r5_*`, `td_r6_*`) | conferência das referências nos documentos | documentação atualizada |

Todos os valores esperados foram conferidos à mão contra o código e a seção 4.3 de `docs/aplicacao.md` (ex.: 30 + 30 × 0,2 + 5 = 41,00; 50 × 0,8 + 5 × 2,50 = 52,50).

### Mutação (baseada em defeitos) — #45

**Ferramenta:** mutmut 3.8.0, Python 3.12, Ubuntu no WSL 2 (o mutmut 3 não roda nativamente no Windows). Configuração `[tool.mutmut]` da issue #36, com a receita de classe isolada acrescentada **só na cópia de execução**, sem versionar:

```toml
only_mutate = ["app/dominio/tarifas.py"]
pytest_add_cli_args_test_selection = ["tests/unit/test_tarifas.py"]
```

**Comandos**

```bash
uv run mutmut run --max-children 4
uv run mutmut results
uv run mutmut show <mutante>
```

**Resultado (22/11/2026)**

| Métrica | 1ª execução — antes (suíte da #41, 118 casos) | 2ª execução — depois (suíte da #46, 125 casos) |
|---|---|---|
| Mutantes gerados | 301 | 301 |
| Mutantes mortos | 278 | **299** |
| Mutantes sobreviventes | 23 | **2** (ambos equivalentes) |
| Timeouts / suspeitos | 0 | 0 |
| **Escore de mutação (mortos / gerados)** | 92,36% | **99,34%** |
| **Escore efetivo (mortos / não equivalentes)** | 278 / 299 = 92,98% | **299 / 299 = 100,00%** |
| Evidência detalhada | [`emprestimo-execucao-1-antes.txt`](evidencias/mutacao/emprestimo-execucao-1-antes.txt) | [`emprestimo-execucao-2-depois.txt`](evidencias/mutacao/emprestimo-execucao-2-depois.txt) |

**Meta da disciplina:** ≥ 80%. ✅ (Atingido: **99,34%** bruto / **100%** descontando equivalentes).

### Triagem dos 23 sobreviventes da 1ª execução e novos testes adicionados

Na 1ª execução com os 118 casos da issue #41, o escore já superava a meta com 92,36% (278 mortos de 301). A análise dos 23 mutantes sobreviventes guiou o acréscimo de 7 novos casos de teste focados em matar mutantes não equivalentes:

| Mutante(s) | Código original → mutado | Classificação | Resolução / Caso adicionado |
|---|---|---|---|
| `__init____mutmut_2` | `teto_comprometimento: float = 0.30` → `1.3` | **Morto na 2ª execução** | `TestConstrutorCustomizado::test_default_valores_construtor` valida os atributos default do construtor. |
| `teto_por_renda__mutmut_1` | `if renda <= 0:` → `if renda < 0:` | **Equivalente** | Para `renda == 0`, o mutante cai em `if renda < 2000: return renda * 0.15` resultando em `0 * 0.15 = 0.0`, idêntico ao `return 0.0`. |
| `parcelas_price__mutmut_5`, `7`, `9` | `round(principal / meses, 2)` com taxa zero → `None`, `()`, `3` | **Mortos na 2ª execução** | `TestParcelas::test_parcelas_price_taxa_zero_divisao_com_dizima` com R$ 100 em 3 meses (dízima R$ 33,33) valida o arredondamento a 2 casas. |
| `parcelas_sac__mutmut_15` | `parcelas.append(round(parcela, 2))` → `round(parcela, 3)` | **Morto na 2ª execução** | `TestParcelas::test_parcelas_sac_arredondamento_fracionario` valida arredondamento com dízima periódica no SAC (R$ 35.83, 35.00, 34.17). |
| `simular__mutmut_80` | `if renda <= 0:` → `if renda <= 1:` | **Morto na 2ª execução** | `TestSimularValidacoes::test_vl_renda_um_real_valida_fronteira` valida que renda de R$ 1,00 é válida (rejeição é `acima_teto`, não `renda_invalida`). |
| `simular__mutmut_144` a `147`, `157` a `159` (7 mutantes) | Retorno em `acima_teto`: alteração de `valor_parcela`, `numero_parcelas`, `total_pago` ou `parcelas` para `None` ou `1` | **Mortos na 2ª execução** | `TestSimularTabelaDecisao::test_td_r8_acima_teto_conferencia_campos_completos` valida todos os 6 atributos da tupla de retorno rejeitada. |
| `simular__mutmut_179` | `if primeira > renda * teto:` → `if primeira >= renda * teto:` | **Morto na 2ª execução** | `TestSimularFronteirasNegocio::test_vl_primeira_parcela_exatamente_igual_teto_comprometimento` testa o limite exato (`primeira == 200.00` e `teto == 200.00`). |
| `simular__mutmut_183` a `186`, `196` a `198` (7 mutantes) | Retorno em `comprometimento_acima`: alteração de atributos para `None` ou `1` | **Mortos na 2ª execução** | `TestSimularTabelaDecisao::test_td_r9_comprometimento_acima_conferencia_campos_completos` valida estritamente todos os atributos do retorno. |
| `simular__mutmut_205` | `total = round(sum(parcelas), 2)` → `round(sum(parcelas), 3)` | **Equivalente** | Como todas as parcelas já foram individualmente arredondadas a duas casas (`round(parcela, 2)`), a soma de números com até duas casas decimais matematicamente termina em centésimos, sendo `round(x, 2) == round(x, 3)` para qualquer conjunto de parcelas. |

### Justificativa dos mutantes equivalentes

1. **`teto_por_renda__mutmut_1`:**
   - No original: `if renda <= 0: return 0.0`.
   - No mutante: `if renda < 0: return 0.0`.
   - Para `renda == 0`: a condição falsa no mutante direciona a execução para o próximo ramo `if renda < 2000: return renda * 0.15`. Como `0.0 * 0.15 = 0.0`, o retorno final é rigorosamente idêntico. O `if renda <= 0` existe como salvaguarda e para manter a complexidade ciclomática da classe.
2. **`simular__mutmut_205`:**
   - No original: `total = round(sum(parcelas), 2)`.
   - No mutante: `total = round(sum(parcelas), 3)`.
   - Em todas as amortizações (Price e SAC), cada elemento de `parcelas` é previamente arredondado com `round(parcela, 2)`. A soma de números com no máximo 2 casas decimais nunca produz dígitos significativos a partir da 3ª casa decimal. Portanto, o arredondamento para 2 ou 3 casas decimais é indistinguível para qualquer entrada válida do domínio.

### Conclusão e lições aprendidas

A suíte unitária de `SimuladorEmprestimo` conta com **125 casos de teste** rigorosos, alcançando **100% de cobertura estrutural de comandos e ramos (todas-arestas)** e **99,34% de escore de mutação bruto** (100% descontando os 2 mutantes equivalentes). A técnica de mutação revelou a importância de conferir não apenas o status booleano e o motivo em cenários de recusa, mas a totalidade dos campos do objeto `ResultadoEmprestimo`, além de testar valores fracionários com dízimas para garantir o arredondamento monetário correto.

| | Piloto da #36 (suíte da Entrega 1, 44 casos) | Execução 1 — antes (suíte da #40, 122 casos) | Execução 3 — depois (suíte da #45, 129 casos) |
|---|---|---|---|
| Mutantes gerados | 106 | 106 | 106 |
| Mortos | 74 | 87 | **100** |
| Sobreviventes | 32 | 19 | 6 (todos equivalentes) |
| Timeout / suspeitos | 0 | 0 | 0 |
| Escore (mortos / gerados) | 69,8% | 82,1% | **94,3%** |
| Escore descontando os equivalentes | — | 87 / 100 = 87,0% | **100 / 100 = 100%** |
| Evidência | [`piloto-tarifas.txt`](evidencias/mutacao/piloto-tarifas.txt) | [`tarifas-execucao-1-antes.txt`](evidencias/mutacao/tarifas-execucao-1-antes.txt) | [`tarifas-execucao-3-final.txt`](evidencias/mutacao/tarifas-execucao-3-final.txt) |

Meta da disciplina: ≥ 80%. ✅ A ampliação da #40 já tinha levado o escore de 69,8% para 82,1%; a #45 eliminou todos os sobreviventes que não são equivalentes. A execução 1 foi feita pelo responsável. Cada arquivo de evidência traz a configuração, os comandos, o resumo e o diff de cada sobrevivente.

**Por que os 13 mutantes sobreviviam:** as tarifas padrão (corrente 30, premium 50, transação 2,50) são valores redondos. Por isso, nenhum teste dependia dos `round(..., 2)`: trocar o arredondamento por `round(x)`, `round(x, None)` ou `round(x, 3)` não mudava nenhum resultado. Os testes novos usam `TarifasBase` com centavos (ex.: premium 50,01, corrente 30,01 e 31). Os valores foram escolhidos para evitar meio centavo exato (x,xx5), em que o arredondamento de `float` é ambíguo.

**Sobreviventes da execução 1 que foram mortos (13)**

| Mutante | Linha original → mutação | Caso que mata |
|---|---|---|
| `tarifa_mensal__mutmut_26`, `_28`, `_29` | `return round(base, 2)` (pacote) → `round(base, None)` / `round(base, )` / `round(base, 3)` | `custom_pacote_premium_arredonda_centavos` (50,01 × 0,7 = 35,007 → 35,01) |
| `tarifa_mensal__mutmut_44`, `_46` | `round(base * 0.8, 2)` → `round(…, None)` / `round(…, )` | `custom_antiguidade_desconto_com_centavos` (31 × 0,8 = 24,80; o mutante dá 25) |
| `tarifa_mensal__mutmut_62` | `round(base + extras, 2)` → `round(…, 3)` | `custom_saldo_negativo_arredonda_resultado_final` (30,01 + 6,002 = 36,012 → 36,01) |
| `_tarifa_com_pacote__mutmut_3` | `saldo >= faixas_isencao[2]` → `saldo > …` | `vl_tarifa_com_pacote_premium_limite_50000` |
| `_tarifa_com_pacote__mutmut_8`, `_10`, `_13` | `round(premium * 0.7, 2)` → `round(…, None)` / `round(…, )` / `round(…, 3)` | `custom_tarifa_com_pacote_premium_centavos` |
| `tarifa_anual__mutmut_1` | padrão `tem_pacote: bool = False` → `True` | `test_pe_anual_premium_com_valores_padrao` (600,00; o mutante dá 420,00) |
| `tarifa_anual__mutmut_4`, `_6` | `round(mensal * 12, 2)` → `round(…, None)` / `round(…, )` | `test_custom_anual_arredonda_centavos` (360,12; o mutante dá 360) |

O mapeamento foi conferido aplicando cada mutante sozinho (`mutmut apply`) e rodando só os testes novos: os 13 são mortos exatamente pelos casos acima ([`tarifas-mapeamento-mutante-teste.txt`](evidencias/mutacao/tarifas-mapeamento-mutante-teste.txt)).

**Sobreviventes equivalentes (6)**

| Mutante | Linha original → mutação | Justificativa |
|---|---|---|
| `tarifa_mensal__mutmut_2` | padrão `quantidade_transacoes: int = 0` → `1` | De 0 a 10 transações a taxa extra é 0; o padrão 1 dá o mesmo resultado que 0 |
| `tarifa_mensal__mutmut_3` | padrão `antiguidade_meses: int = 0` → `1` | As regras só mudam em 24 e 36 meses; 1 mês se comporta igual a 0 |
| `tarifa_mensal__mutmut_49` | `round(base * 0.8, 2)` → `round(…, 3)` | O `round(…, 2)` final desfaz a diferença. Verificado para todas as tarifas de R$ 0,01 a R$ 20.000,00 em passos de 1 centavo: nenhum valor distingue o mutante |
| `tarifa_por_transacao_extra__mutmut_1` | `quantidade <= transacoes_gratuitas` → `<` | Com exatamente 10 transações, o mutante calcula (10 − 10) × 2,50 = 0, o mesmo `0.0` do original |
| `tarifa_anual__mutmut_2` | padrão `quantidade_transacoes: int = 0` → `1` | Mesmo raciocínio do `tarifa_mensal__mutmut_2` |
| `tarifa_anual__mutmut_17` | `round(mensal * 12, 2)` → `round(…, 3)` | A mensal já vem arredondada a 2 casas, e × 12 continua com no máximo 2 casas. Verificado de R$ 0,01 a R$ 20.000,00: nenhum valor distingue |

**Observação:** 4 dos 13 mutantes mortos estão em `_tarifa_com_pacote`, que é **código morto** (apontado na #40 para a #50). Se a #50 remover o método, os testes dele saem junto e o escore deve ser recalculado sobre os mutantes restantes.

> **Atualização (#50, 22/11/2026):** a #50 removeu `_tarifa_com_pacote` e reescreveu `tarifa_mensal` sem aninhamento (correção do Sonar `python:S3776`). Os testes do método removido passaram a verificar a mesma regra por `tarifa_mensal` com pacote, e foi acrescentado o caso `custom_pacote_meia_tarifa_com_centavos`. Nova execução: **101 mutantes, 93 mortos (92,1%)**. Dos 8 sobreviventes, 7 são equivalentes — os 6 da tabela acima (com outros números, porque o código mudou) e 1 novo, o padrão `antiguidade_meses` 0 → 1 de `tarifa_anual` (mesmo raciocínio do `tarifa_mensal__mutmut_3`) — e 1 é `round(corrente * 0.5, 2)` → `round(..., 3)` na meia tarifa, que só se distingue em meio centavo exato (ambíguo em `float`) e não recebeu teste frágil. Evidência: [`tarifas-execucao-4-pos-sonar.txt`](evidencias/mutacao/tarifas-execucao-4-pos-sonar.txt).

**Revisão da solução gerada por IA** ([sessão 21 do AI-LOG](../ai/prompts/sessao-21-mutacao-tarifas.md)): a solução inicial (commit `145bd2d`, [`tarifas-execucao-2-solucao-inicial.txt`](evidencias/mutacao/tarifas-execucao-2-solucao-inicial.txt)) já matava os 13 mutantes. A revisão conferiu o mapeamento mutante → teste e corrigiu três pontos de manutenção (commit `21e9824`): os comentários citavam só o número do mutante, que muda quando `tarifas.py` muda, e passaram a descrever a mutação; faltava o aviso de que os testes de `_tarifa_com_pacote` cobrem código morto; e faltava a justificativa dos valores com centavos.

---

## `TransacaoPix` — `app/dominio/pix.py`

| Campo | Valor |
|---|---|
| Responsável | Alexandre Colmenero |
| Issues | #38 (unitários + cobertura estrutural) · #43 (mutação) |
| Arquivo de testes | `tests/unit/test_pix.py` |
| Complexidade ciclomática (soma dos métodos, `radon cc`) | 52 |

### Cobertura estrutural (todas-arestas) — #38

**Comando**

```bash
uv run pytest tests/unit/test_pix.py --cov=app.dominio.pix --cov-branch --cov-report=term-missing
```

**Antes × depois**

| | Antes (Entrega 1) | Depois (22/11/2026 — #38) |
|---|---|---|
| Casos de teste | 68 | 104 |
| Resultado | 66 passam · 2 falham (#16, #17) | 104 passam |
| Cobertura de arestas | 100% | **100%** |
| Linhas / ramos não cobertos | nenhuma (101 stmts, 50 branches) | nenhuma (101 stmts, 50 branches) |

**Saída (depois)**

```text
Name                 Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------
app/dominio/pix.py     101      0     50      0   100%
----------------------------------------------------------------
TOTAL                  101      0     50      0   100%
Required test coverage of 80.0% reached. Total coverage: 100.00%
104 passed in 0.40s
```

A cobertura já era de 100% na Entrega 1; a ampliação reorganizou a suíte por técnica e acrescentou 36 casos que exercitam as fronteiras que a mutação (#43) tende a atacar. Os 2 casos que falhavam na Entrega 1 eram os defeitos #16 e #17, corrigidos no commit `e7881bd` (PR #89) e mantidos na suíte como regressão (`email_dois_arroba` e `chargeback_bloqueada_dias_30_valor_alto`).

### Técnicas funcionais aplicadas

A técnica de cada caso novo está no prefixo do id do `pytest.param`.

| Técnica | Prefixo | Casos | Onde |
|---|---|---|---|
| Partição de equivalência | `pe_` | 5 | CPF formatado e com letras; e-mail com três `@`; aleatória com espaços; `autorizar` sem saldo (`saldo=None`) |
| Análise de valor-limite | `vl_` | 9 | limites diurnos/noturnos a ±0,01; horário 19:59/20:00/5:59/6:00/6:01; saldo a ±0,01 do valor |
| Tabela de decisão | `td_` | 8 | precedências de `autorizar` e combinações de chave bloqueada/motivo/faixas do chargeback |
| Teste de laços | `laco_` | 2 | CPF que falha no 1º e no 2º dígito verificador |
| Parâmetros customizados | `custom_` | 8 | limites próprios de `autorizar` e prazo/teto próprios do chargeback |
| Janela noturna com virada de dia | sem prefixo | 4 | `noturno_custom_virada_*` (22h–2h) |
| Regressão de defeitos | ids originais | 2 | `email_dois_arroba` (#16) e `chargeback_bloqueada_dias_30_valor_alto` (#17) |

> Os 68 casos da Entrega 1 mantiveram os ids originais (sem prefixo) para preservar as referências das issues #16 e #17.

**Observações de projeto:**

- **Isolamento de dependências:** não se aplica — `TransacaoPix` é uma classe pura, sem repositório ou framework; o isolamento por mock ficou nos serviços (#53).
- **Determinismo:** `autorizar` usa `datetime.now()` quando o horário não é informado; todos os casos de caminho válido passam `horario` fixo.

### Mutação (baseada em defeitos) — #43

**Ferramenta:** `mutmut` 3.8.0, com a receita de **classe isolada** da issue #36 (acrescentada temporariamente ao `pyproject.toml`, sem versionar, e removida após a medição):

```toml
only_mutate = ["app/dominio/pix.py"]
pytest_add_cli_args_test_selection = ["tests/unit/test_pix.py"]
```

**Comandos**

```bash
rm -rf .mutmut-cache mutants   # força a re-execução com a suíte nova
uv run mutmut run --max-children 4
uv run mutmut results
uv run mutmut show <mutante>
```

**Resultado (22/11/2026)**

| | 1ª execução — antes (suíte da #38, 104 casos) | 2ª execução — depois (suíte da #43, 111 casos) |
|---|---|---|
| Mutantes gerados | 148 | 148 |
| Mortos | 136 | **144** |
| Sobreviventes | 12 | 4 (todos equivalentes) |
| Timeout / suspeitos | 0 | 0 |
| Escore (mortos / gerados) | 91,9% | **97,3%** |
| Escore descontando os equivalentes (mortos / não equivalentes) | 136 / 140 = 97,1% | **144 / 144 = 100%** |
| Evidência | [`pix-execucao-1-antes.txt`](evidencias/mutacao/pix-execucao-1-antes.txt) | [`pix-execucao-2-depois.txt`](evidencias/mutacao/pix-execucao-2-depois.txt) |

Meta da disciplina: ≥ 80%. ✅

**Triagem dos 12 sobreviventes da 1ª execução**

| Mutante | Linha original → mutação | Classificação | Caso que mata |
|---|---|---|---|
| `autorizar__mutmut_4` | `valor <= 0` → `valor <= 1` | Morto na 2ª execução | `vl_valor_um_real` (valor 1,00 é válido) |
| `solicitar_chargeback__mutmut_7` | `valor <= 0` → `valor <= 1` | Morto na 2ª execução | `vl_chargeback_valor_um_real` |
| `solicitar_chargeback__mutmut_23` | `dias <= 7` → `dias < 7` | Morto na 2ª execução | `vl_chargeback_dias_7_valor_alto` (7 dias com valor acima do teto: o original aprova antes da regra de valor) |
| `_eh_noturno__mutmut_1` | `inicio <= fim` → `inicio < fim` | Morto na 2ª execução | `vl_janela_ponto_depois` (janela com início == fim) |
| `_validar_cpf__mutmut_16` | `range(9, 11)` → `range(10, 11)` | Morto na 2ª execução | `laco_cpf_falha_so_primeiro_dv` (CPF que falha só no 1º dígito verificador) |
| `_validar_cpf__mutmut_34` | `resto == 10` → `resto == 11` | Morto na 2ª execução | `pe_cpf_valido_dv_zero` (resto 10 no 2º DV, transformado em 0) |
| `_validar_cpf__mutmut_35` | `resto = 0` → `resto = None` | Morto na 2ª execução | `pe_cpf_valido_dv_zero` |
| `_validar_cpf__mutmut_36` | `resto = 0` → `resto = 1` | Morto na 2ª execução | `pe_cpf_valido_dv_zero` |
| `validar_chave__mutmut_3` | `(chave or "")` → `(chave or "XXXX")` | Equivalente | — |
| `solicitar_chargeback__mutmut_14` | `(motivo or "")` → `(motivo or "XXXX")` | Equivalente | — |
| `_validar_cpf__mutmut_9` | `digitos == digitos[0] * 11` → `digitos == digitos[1] * 11` | Equivalente | — |
| `_validar_email__mutmut_8` | `partition("@")` → `rpartition("@")` | Equivalente | — |

O mapeamento mutante → teste foi conferido aplicando cada mutante sozinho (`mutmut apply`) e rodando só o teste indicado: 8/8 mortos (registrado na evidência).

**Justificativa dos 4 equivalentes**

- `validar_chave__mutmut_3` e `solicitar_chargeback__mutmut_14`: a mutação só altera o valor usado quando o argumento é `None`/falsy. `"XXXX"` não valida como chave de nenhum tipo (CPF, e-mail, telefone ou aleatória de 32) e não contém `golpe`/`fraude` — o resultado é sempre o mesmo.
- `_validar_cpf__mutmut_9`: em uma string de 11 caracteres, `digitos == digitos[0] * 11` e `digitos == digitos[1] * 11` só são verdadeiras quando todos os dígitos são iguais; as condições são idênticas.
- `_validar_email__mutmut_8`: a linha só é alcançada quando `email.count("@") == 1`, caso em que `partition` e `rpartition` devolvem exatamente a mesma divisão.

**Lição registrada:** a cobertura de arestas já era 100%, mas a mutação revelou fronteiras não testadas — valor `1,00` (mutação de `<= 0` para `<= 1`), 7 dias com valor acima do teto, janela noturna com início == fim e o ramo `resto == 10` do CPF (que exige um CPF válido com dígito verificador 0).

Evidência da cobertura: [`evidencias/cobertura/pix-cobertura.txt`](evidencias/cobertura/pix-cobertura.txt).
