# Sessão 19 — Testes unitários e cobertura estrutural de `TarifaBancaria` (issue #40)

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielcamposs`) |
| Data | 22/11/2026 |
| Ferramenta | Claude Code (extensão do VS Code), modelo Claude Opus 5.5 (`claude-opus-5-5`) / Terminal (`uv run pytest`) |
| Atividade | Ampliar casos de teste unitários e comprovar cobertura estrutural todas-arestas de `TarifaBancaria` (issue #40); abrir issues para os defeitos revelados |
| Artefatos | `tests/unit/test_tarifas.py` |

## Contexto

Ampliar os testes unitários da classe `TarifaBancaria` (`app/dominio/tarifas.py`) em `tests/unit/test_tarifas.py` para a issue #40, aplicando partição de equivalência (`pe_`), análise de valor-limite (`vl_`) e tabela de decisão (`td_`), e cobrindo a aresta que faltava (linha 49: desconto de 20% com antiguidade ≥ 36 meses). A classe não possui laços, então o teste de laços não se aplica.

A sessão teve duas rodadas. Na **rodada 1**, a IA planejou e executou a issue a partir do relatório de issues da Entrega 2 (seção B3) e do enunciado, com prompts de conversa do responsável. Esses prompts foram: "esse é o plano da entrega, voce deve seguir totalmente esse plano"; "me fale exatamente o que voce vai fazer na #40 qual seu plano de realmente executa-la"; "tudo isso esta sendo incluido nessa issue?"; "voce deve se orientar por 2 arquivos, de enfase para o registro do uso da ia"; "nao entendi o item 1"; "faça pelo plano A, como voce planeja seguir com o registro dos prompts e ai-log.md eu preciso que voce siga estritamente isso". Em seguida o responsável revisou o trabalho ("quero revisar o que a ia fez"; "como faço para rodar a aplicação e simular o que ia implementou?") e, na **rodada 2**, enviou o prompt técnico abaixo.

## Prompt utilizado

> "Analise os códigos abaixo de app/dominio/tarifas.py e tests/unit/test_tarifas.py. Atualmente a suíte tem 44 testes passando e 97% de cobertura de arestas: a linha 49 (base = round(base * 0.8, 2), desconto de 20% para antiguidade_meses >= 36 sem pacote) nunca é executada, porque nenhum teste passa antiguidade_meses.
>
> Revise os casos existentes e amplie tests/unit/test_tarifas.py com novos casos relevantes aplicando explicitamente:
>
> Partição de equivalência (pe_): tipo de conta (corrente, poupança, premium), com e sem pacote, saldo negativo / zero / positivo.
> Análise de valor-limite (vl_): faixas de isenção (999,99 / 1000 / 4999,99 / 5000 / 49999,99 / 50000), antiguidade (23 / 24 / 35 / 36 meses), cota de transações gratuitas (10 / 11) e saldo (−0,01 / 0).
> Tabela de decisão (td_): em tarifa_mensal sem pacote, combinar isenção por saldo × antiguidade ≥ 36 × saldo negativo × transações extras, respeitando a precedência do if/elif (isenção > antiguidade > saldo negativo). Em tarifa_mensal com pacote, combinar tipo × saldo ≥ 50000 × saldo ≥ 5000 × antiguidade ≥ 24."

**Resposta da IA:** comparou o prompt com a suíte da rodada 1 (97 casos) e encontrou três lacunas: 9 das 18 combinações tipo × pacote × saldo sem caso; a faixa 999,99/1000 testada só em `_tem_isencao`, nunca em `tarifa_mensal`; e tabelas de decisão incompletas. Acrescentou os casos `pe_` e `vl_` que faltavam e substituiu a tabela de decisão anterior por duas tabelas completas. A tabela sem pacote tem as 12 combinações possíveis, porque isenção e saldo negativo são mutuamente exclusivos. A tabela com pacote tem 2 tipos × 3 faixas de saldo × 2 antiguidades; as 3 combinações premium da regra R3 entraram no teste do defeito #78. A suíte foi a 119 casos.

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações quando a IA é usada na geração de testes. Em cada rodada, a solução da IA foi gravada em commit **antes** de qualquer revisão. Os diffs entre inicial e final estão em [`sessao-19-diff-solucao-inicial-final.diff`](sessao-19-diff-solucao-inicial-final.diff) (rodada 1) e [`sessao-19-diff-prompt-tecnico-inicial-final.diff`](sessao-19-diff-prompt-tecnico-inicial-final.diff) (rodada 2).

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| **Rodada 1** (commit `70ccd5c`): suíte ampliada de 44 para 98 casos, **95 passando e 3 `xfail`**, **100%** de cobertura de arestas. Tinha 2 casos duplicados, faltava a partição inválida de antiguidade, `tarifa_anual` era testada com oráculo calculado pelo próprio código (`tarifa_mensal(...) * 12`) e o `xfail` do defeito da anual aceitava qualquer exceção | **Rodada 1** (commit `ee613a6`): 97 casos, **94 passando e 3 `xfail`**, **100%** | Removidos `pe_corrente_saldo_zero` e `pe_corrente_pacote_antiguidade_nova` (duplicados); acrescentado `pe_antiguidade_negativa_sem_validacao`; `tarifa_anual` passou a ter valores explícitos (0; 180; 420; 462); `xfail` da anual restrito com `raises=TypeError`; `reason` com os números das issues #77 e #78 |
| **Rodada 2** (commit `eaafc09`): suíte com 119 casos, **115 passando e 4 `xfail`**, **100%**. Ao substituir a tabela de decisão antiga, perdeu 3 cenários da premium sem pacote (isenção no limite 50000 com antiguidade, antiguidade com saldo negativo, antiguidade com extras), porque a nova tabela sem pacote usava só a conta corrente | **Rodada 2** (commit `3809dcc`): **122 casos, 118 passando e 4 `xfail`**, **100%** de cobertura de arestas (`54` statements, `0` missed, `24` branches, `0` partial) | `test_tarifa_mensal_tabela_decisao_sem_pacote` passou a receber o tipo de conta, com 3 linhas `td_sp_premium_*` (0,00; 40,00; 52,50); referências a ids removidos (`td_r1_*`, `td_r5_*`, `td_r6_*`) atualizadas no relatório e no Plano de Teste |

**Como os problemas foram encontrados:** nenhum aparecia na execução, porque as duas soluções iniciais passavam e já tinham 100% de arestas. Os duplicados e os cenários perdidos foram achados comparando os parâmetros dos casos. A partição inválida foi achada revisando as classes de equivalência. O oráculo fraco foi comprovado por mutação manual temporária em `tarifas.py` (`corrente * 0.5` → `corrente * 0.6`, depois revertida): o teste inicial **continuou passando** (`4 passed`) e o final falhou (`assert 216.0 == 180.0`), conforme [`tarifas-verificacao-oraculo-anual.txt`](../../relatorios/evidencias/cobertura/tarifas-verificacao-oraculo-anual.txt). O `xfail` amplo foi achado executando com `--runxfail`.

**Decisão:** a estrutura e os valores esperados gerados pela IA foram aceitos depois de conferidos à mão contra o código e a seção 4.3 de `docs/aplicacao.md` (ex.: 30 + 30 × 0,2 + 5 = 41,00; 50 × 0,8 + 5 × 2,50 = 52,50); os problemas acima foram corrigidos em `tests/unit/test_tarifas.py`. As linhas das tabelas de decisão que coincidem com casos `vl_` ou da Entrega 1 foram **mantidas de propósito**, para cada tabela ficar completa. Duas divergências da especificação foram abertas como issues de bug: [#77](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/77) e [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78). Os testes correspondentes ficaram com `xfail(strict=True)`, para não bloquear o mutmut da #45. O código de domínio em `app/dominio/tarifas.py` foi mantido sem alterações. O reagrupamento dos 44 casos da Entrega 1 por técnica, proposto no plano da rodada 1, não foi feito.

**Validação inicial:** `uv run pytest tests/unit/test_tarifas.py --cov=app.dominio.tarifas --cov-branch --cov-report=term-missing -rxX` → rodada 1: `95 passed, 3 xfailed in 0.73s`; rodada 2: `115 passed, 4 xfailed in 0.77s` (`100%` de cobertura nas duas). Evidências: [`tarifas-1-solucao-inicial.txt`](../../relatorios/evidencias/cobertura/tarifas-1-solucao-inicial.txt) e [`tarifas-3-prompt-tecnico-inicial.txt`](../../relatorios/evidencias/cobertura/tarifas-3-prompt-tecnico-inicial.txt).

**Validação final:** `uv run pytest tests/unit/test_tarifas.py --cov=app.dominio.tarifas --cov-branch --cov-report=term-missing -rxX` → `118 passed, 4 xfailed in 0.75s` (`100%` de cobertura: `54` statements, `0` missed, `24` branches, `0` partial). Evidência: [`tarifas-4-prompt-tecnico-final.txt`](../../relatorios/evidencias/cobertura/tarifas-4-prompt-tecnico-final.txt). Defeitos: `uv run pytest tests/unit/test_tarifas.py -k defeito --runxfail` → `4 failed` (`TypeError: ... unexpected keyword argument 'antiguidade_meses'` e 3× `AssertionError: assert 15.0 == 25.0`), em [`tarifas-defeitos-runxfail.txt`](../../relatorios/evidencias/cobertura/tarifas-defeitos-runxfail.txt). Também: `uv run ruff check tests/unit/test_tarifas.py` → `All checks passed!`; `uv run radon cc app/dominio/tarifas.py -s` → `tarifa_mensal - C (12)`, inalterado; `uv run pytest tests/unit` → `2 failed, 404 passed, 4 xfailed`. As 2 falhas são os bugs #16 e #17 (PIX), que já existiam antes desta sessão.

## Ações executadas

1. Analisadas as regras de `TarifaBancaria` em `app/dominio/tarifas.py`, a suíte em `tests/unit/test_tarifas.py` e a cobertura inicial (`44 passed`, 97%, linha 49 faltando).
2. Rodada 1: adicionados casos `pe_`, `vl_`, `td_` e `custom_` e 3 casos de defeito com `xfail`; solução gravada sem revisão (`70ccd5c`), revisada e gravada (`ee613a6`).
3. Executados os casos de defeito com `--runxfail` e abertas as issues [#77](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/77) e [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78), com a falha como evidência.
4. Preparada a revisão pelo responsável: aplicação executada (`uv run flask --app app:create_app run`, com banco temporário) e roteiro de casos para conferir na tela de tarifas e no interpretador Python.
5. Rodada 2 (prompt técnico): completadas as combinações `pe_` de tipo × pacote × saldo, a faixa 999,99/1000 em `tarifa_mensal` e as duas tabelas de decisão completas; solução gravada sem revisão (`eaafc09`).
6. Revisada a rodada 2: recuperados os 3 cenários da premium perdidos na troca das tabelas; solução gravada (`3809dcc`).
7. Reexecutada a suíte completa (`118 passed, 4 xfailed`, 100%) e atualizados `docs/relatorios/cobertura_mutacao.md` (seção `TarifaBancaria`), `docs/plano_de_teste.md` (v1.14, seção 6.8) e o AI-LOG.

## Resultado

- **122 casos** em `tests/unit/test_tarifas.py` (antes: 44): **118 aprovados e 4 `xfail`** (`0.75s`): 21 `pe_`, 25 `vl_`, 29 `td_`, 2 `custom_` e 1 caso de defeito, além dos 44 da Entrega 1.
- Cobertura estrutural todas-arestas de **97% → 100%** (`54` statements, `0` missed, `24` branches, `0` partial); linha 49 coberta.
- **2 defeitos revelados**, abertos como issues: [#77](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/77) (`tarifa_anual` ignora a antiguidade: esperado 288,00, atual sempre 360,00) e [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78) (meia tarifa do pacote premium usa a tarifa da corrente: esperado 25,00, atual 15,00; a confirmar pelo grupo).
- Observações para a #50 (Sonar), sem issue de bug: `_tarifa_com_pacote` é código morto, e a faixa de isenção da poupança (1000) nunca é consultada por `tarifa_mensal`.
