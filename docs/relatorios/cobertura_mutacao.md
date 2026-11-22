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

Os casos foram gerados com apoio do Claude Code ([sessão 18 do AI-LOG](../ai/prompts/sessao-18-cobertura-tarifas.md)) em duas rodadas. Cada rodada teve a solução da IA gravada sem revisão e depois revisada:

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
