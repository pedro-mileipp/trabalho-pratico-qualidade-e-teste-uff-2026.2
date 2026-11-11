# Relatório de Cobertura Estrutural e Mutação — Entrega 2

Resultados das técnicas **estrutural** (critério todas-arestas, meta ≥ 80%) e **baseada em defeitos** (escore de mutação, meta ≥ 80%) por classe de domínio.

> As seções das demais classes são adicionadas pelos responsáveis de cada issue. A configuração padrão de cobertura e do mutmut é tratada na issue #36.

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

### Mutação — #47

_A preencher na issue #47._
