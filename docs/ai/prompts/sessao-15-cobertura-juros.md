# Sessão 15 — Testes unitários e cobertura estrutural de `CalculadoraJuros` (issue #39)

| Campo | Valor |
|---|---|
| Responsável | Gabrielle Rosa (`n2Gabrielle`) |
| Data | 20/11/2026 |
| Ferramenta | Gemini / VS Code / Terminal (`.venv/bin/pytest`) |
| Atividade | Ampliar casos de teste unitários e comprovar cobertura estrutural todas-arestas de `CalculadoraJuros` (issue #39) |
| Artefatos | `tests/unit/test_juros.py` |

## Contexto

Ampliar os testes unitários da classe `CalculadoraJuros` (`app/dominio/juros.py`) em `tests/unit/test_juros.py` para a issue #39, aplicando partição de equivalência (`pe_`), análise de valor-limite (`vl_`), tabela de decisão (`td_`) e teste de laços (`laco_`), mantendo a cobertura estrutural (todas-arestas) em 100% após a correção da issue #20.

## Prompt utilizado

> "Analise os códigos abaixo de `app/dominio/juros.py` e `tests/unit/test_juros.py`.
> Atualmente a suíte tem 36 testes passando e já atingiu 100% de cobertura de linhas e ramos (67 statements, 0 missed, 36 branches, 0 partial) após a correção do desconto de IR no mês 12 (issue #20).
>
> Revise os casos existentes e amplie `tests/unit/test_juros.py` com novos casos relevantes aplicando explicitamente:
> - Partição de equivalência (`pe_`)
> - Análise de valor-limite (`vl_`)
> - Tabela de decisão (`td_`)
> - Teste de laços (`laco_`, incluindo prazos maiores que 12 meses e diferentes quantidades de iterações)
>
> Identifique claramente a técnica aplicada no `id` de cada `pytest.param` ou em comentário, sem quebrar os testes já aprovados e sem alterar `app/dominio/juros.py` (salvo se algum teste revelar um defeito real ainda não reportado)."

**Resposta da IA:** revisou `app/dominio/juros.py` e `tests/unit/test_juros.py` e adicionou novos casos parametrizados e unitários com identificadores das técnicas `pe_`, `vl_`, `td_` e `laco_` (elevando a suíte de 36 para 68 casos).

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações quando a IA é usada na geração de testes.

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| Suíte ampliada para 68 casos, com 16 falhas nos novos casos devido a expectativas calculadas incorretamente ou parâmetros (`taxa_anual=0.0` no teste da trava de R$ 1.000.000) | Suíte com 68 casos aprovados e **100.00%** de cobertura de linhas e ramos (`67` statements, `0` missed, `36` branches, `0` partial) | Revisados os valores esperados em `test_total_a_pagar_pe_e_vl` (mora aplicada sobre o montante composto), `test_montante_com_aportes_tabela_decisao` (`td_r1` e `td_r2` conforme capitalização mensal no laço), `test_calcular_montante_lacos` (taxa da faixa e capitalização mensal) e ajustada a `taxa_anual=0.12` em `test_montante_com_aportes_vl_trava_um_milhao_estrita` para alcançar o laço de juros e a trava de R$ 1.000.000 |

**Decisão:** todas as 16 falhas iniciais foram classificadas como expectativas incorretas nos casos recém-gerados (e não defeitos de `CalculadoraJuros`), sendo corrigidas em `tests/unit/test_juros.py`; o código de domínio em `app/dominio/juros.py` foi mantido sem alterações.

**Validação inicial:** `.venv/bin/pytest tests/unit/test_juros.py --cov=app.dominio.juros --cov-branch --cov-report=term-missing -v` → `16 failed, 52 passed in 0.60s` (`100.00%` de cobertura).

**Validação final:** `.venv/bin/pytest tests/unit/test_juros.py --cov=app.dominio.juros --cov-branch --cov-report=term-missing -v` → `68 passed in 0.40s` (`100.00%` de cobertura: `67` statements, `0` missed, `36` branches, `0` partial)[cite: 7].

## Ações executadas

1. Analisadas as regras de `CalculadoraJuros` em `app/dominio/juros.py` e a suíte em `tests/unit/test_juros.py`.
2. Adicionados os novos casos com prefixos/identificadores de `pe_`, `vl_`, `td_` e `laco_`.
3. Executada a suíte com `--cov=app.dominio.juros --cov-branch --cov-report=term-missing` e inspecionadas as 16 falhas iniciais.
4. Corrigidas as expectativas e os parâmetros dos novos testes e reexecutada a suíte completa (`68 passed in 0.40s`, `100.00%` de cobertura)[cite: 7].

## Resultado

- **68 casos aprovados** em `tests/unit/test_juros.py` (`0.40s`)[cite: 7].
- Cobertura estrutural (todas-arestas / linhas e ramos) mantida em **100.00%** (`67` statements, `0` missed, `36` branches, `0` partial)[cite: 7].
- Nenhum defeito novo encontrado em `app/dominio/juros.py`.