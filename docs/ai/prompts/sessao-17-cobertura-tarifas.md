# Sessão 17 — Testes unitários e cobertura estrutural de `TarifaBancaria` (issue #40)

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielcamposs`) |
| Data | 22/11/2026 |
| Ferramenta | Claude Code (extensão do VS Code), modelo Claude Opus 5.5 (`claude-opus-5-5`) / Terminal (`uv run pytest`) |
| Atividade | Ampliar casos de teste unitários e comprovar cobertura estrutural todas-arestas de `TarifaBancaria` (issue #40); abrir issues para os defeitos revelados |
| Artefatos | `tests/unit/test_tarifas.py`; `docs/relatorios/cobertura_mutacao.md`; `docs/relatorios/evidencias/cobertura/tarifas-*.txt`; `docs/plano_de_teste.md`; issues #77 e #78 |

## Contexto

Ampliar os testes unitários da classe `TarifaBancaria` (`app/dominio/tarifas.py`) em `tests/unit/test_tarifas.py` para a issue #40, aplicando partição de equivalência (`pe_`), análise de valor-limite (`vl_`) e tabela de decisão (`td_`), e cobrir a aresta que faltava: linha 49, desconto de 20% com antiguidade ≥ 36 meses. Antes da sessão a suíte tinha 44 casos passando e 97% de cobertura de arestas. A classe não possui laços, então o teste de laços não se aplica.

A IA foi orientada pelo relatório de issues da Entrega 2 (`relatorio_issues_entrega_2.md`, seção B3) e pelo enunciado do trabalho (`instrucoes_trabalho.md`).

## Prompt utilizado

Prompts do responsável, na ordem em que foram enviados (transcrição literal):

> 1. (com o relatório de issues da Entrega 2 anexado) "esse é o plano da entrega, voce deve seguir totalmente esse plano"
> 2. "me fale exatamente o que voce vai fazer na #40 qual seu plano de realmente executa-la"
> 3. (com print da issue #40) "tudo isso esta sendo incluido nessa issue?"
> 4. (com o enunciado e o relatório de issues anexados) "voce deve se orientar por 2 arquivos, de enfase para o registro do uso da ia"
> 5. "nao entendi o item 1"
> 6. "faça pelo plano A, como voce planeja seguir com o registro dos prompts e ai-log.md eu preciso que voce siga estritamente isso"
> 7. "quero revisar o que a ia fez"
> 8. "como faço para rodar a aplicação e simular o que ia implementou?"
> 9. (com print do navegador: `ERR_CONNECTION_REFUSED` em `127.0.0.1:5000`)
> 10. (com a sessão 15 colada como modelo) "queria que voce seguisse esse modelo para registro nos prompts e realização da issue"

**Resposta da IA:** leu a issue #40, `app/dominio/tarifas.py` e `tests/unit/test_tarifas.py`, mediu a cobertura (97%, linha 49 faltando) e apresentou um plano relacionando cada item da issue a uma etapa (prompts 1–3). Apontou 3 suspeitas de defeito: `tarifa_anual` sem antiguidade, meia tarifa do pacote premium calculada sobre a corrente e `_tarifa_com_pacote` nunca chamado. Propôs tratar os defeitos com teste que falha, issue de bug e `xfail(strict=True)` para não bloquear o mutmut da #45 (prompt 5, "plano A"). Depois de autorizada (prompt 6), ampliou a suíte de 44 para 98 casos com identificadores `pe_`, `vl_`, `td_` e `custom_`, gravou essa versão sem revisão, revisou e chegou a 97 casos. Nos prompts 7–9, orientou a revisão humana, explicou como rodar a aplicação (`uv run flask --app app:create_app run` com banco temporário) e quais casos aparecem na tela de tarifas, e subiu o servidor quando o navegador acusou conexão recusada. No prompt 10, reorganizou este registro no formato da sessão 15.

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações quando a IA é usada na geração de testes. A solução inicial está no commit `04f2296` e a final no `bb5025b`; o diff está em [`sessao-17-diff-solucao-inicial-final.diff`](sessao-17-diff-solucao-inicial-final.diff).

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| Suíte ampliada para 98 casos (54 novos), com **95 passando e 3 `xfail`** e **100%** de cobertura de arestas. Passava de primeira, mas tinha 2 casos duplicados, faltava a partição inválida de antiguidade, `tarifa_anual` era testada com oráculo calculado pelo próprio código (`tarifa_mensal(...) * 12`) e o `xfail` do defeito da anual aceitava qualquer exceção | Suíte com 97 casos (53 novos): **94 passando e 3 `xfail`** que documentam os defeitos #77 e #78; **100%** de cobertura de arestas (`54` statements, `0` missed, `24` branches, `0` partial) | Removidos `pe_corrente_saldo_zero` (= `vl_saldo_zero_sem_sobretaxa`) e `pe_corrente_pacote_antiguidade_nova` (= `td_r4_corrente_pacote`); acrescentado `pe_antiguidade_negativa_sem_validacao`; `test_tarifa_anual_igual_a_doze_mensais` substituído por `test_tarifa_anual_particao_equivalencia`, com valores explícitos (0; 180; 420; 462); `xfail` da anual restrito com `raises=TypeError`; `reason` dos `xfail` com os números das issues #77 e #78 |

**Como os problemas foram encontrados:** nenhum aparecia na execução. Os duplicados foram achados comparando os parâmetros dos casos. A partição inválida faltando foi achada revisando as classes de equivalência. O oráculo fraco foi comprovado com uma mutação manual temporária em `tarifas.py` (`corrente * 0.5` → `corrente * 0.6`, depois revertida): o teste inicial **continuou passando** (`4 passed`) e o final falhou (`assert 216.0 == 180.0`), conforme [`tarifas-verificacao-oraculo-anual.txt`](../../relatorios/evidencias/cobertura/tarifas-verificacao-oraculo-anual.txt). O `xfail` amplo foi achado executando com `--runxfail`, que mostrou que a falha real era `TypeError`.

**Decisão:** a estrutura e os valores esperados gerados pela IA foram aceitos, depois de conferidos à mão contra o código e a seção 4.3 de `docs/aplicacao.md` (ex.: 30 × 0,8 = 24,00; 50 × 0,8 + 5 × 2,50 = 52,50). Os problemas acima foram corrigidos em `tests/unit/test_tarifas.py`. Duas falhas revelaram comportamento divergente da especificação e foram abertas como issues de bug (#77 e #78), com o teste marcado `xfail(strict=True)`. O código de domínio em `app/dominio/tarifas.py` foi mantido sem alterações. O reagrupamento dos 44 casos da Entrega 1 por técnica, proposto no plano, não foi feito; só o id `premium_pacote_isencao_5x5` foi renomeado para `premium_pacote_isento_saldo_limite_50000`.

**Validação inicial:** `uv run pytest tests/unit/test_tarifas.py --cov=app.dominio.tarifas --cov-branch --cov-report=term-missing -rxX` → `95 passed, 3 xfailed in 0.73s` (`100%` de cobertura). Evidência: [`tarifas-1-solucao-inicial.txt`](../../relatorios/evidencias/cobertura/tarifas-1-solucao-inicial.txt).

**Validação dos defeitos:** `uv run pytest tests/unit/test_tarifas.py -k defeito --runxfail` → `3 failed` (`TypeError: TarifaBancaria.tarifa_anual() got an unexpected keyword argument 'antiguidade_meses'` e 2× `AssertionError: assert 15.0 == 25.0`). Evidência: [`tarifas-defeitos-runxfail.txt`](../../relatorios/evidencias/cobertura/tarifas-defeitos-runxfail.txt).

**Validação final:** `uv run pytest tests/unit/test_tarifas.py --cov=app.dominio.tarifas --cov-branch --cov-report=term-missing -rxX` → `94 passed, 3 xfailed in 0.77s` (`100%` de cobertura: `54` statements, `0` missed, `24` branches, `0` partial). Evidência: [`tarifas-2-solucao-final.txt`](../../relatorios/evidencias/cobertura/tarifas-2-solucao-final.txt). Também: `uv run ruff check tests/unit/test_tarifas.py` → `All checks passed!`; `uv run radon cc app/dominio/tarifas.py -s` → `tarifa_mensal - C (12)`, inalterado; `uv run pytest tests/unit` → `2 failed, 380 passed, 3 xfailed`. As 2 falhas são os bugs #16 e #17 (PIX), que já existiam antes desta sessão.

## Ações executadas

1. Analisadas as regras de `TarifaBancaria` em `app/dominio/tarifas.py`, a suíte em `tests/unit/test_tarifas.py` e a cobertura inicial (`44 passed`, 97%, linha 49 faltando).
2. Criada a branch `test/issue-40-cobertura-tarifas` e adicionados os novos casos com os prefixos `pe_`, `vl_`, `td_` e `custom_`, mais 3 casos de defeito com `xfail`.
3. Executada a suíte com `--cov=app.dominio.tarifas --cov-branch --cov-report=term-missing`; solução inicial gravada sem revisão (commit `04f2296`).
4. Executados os casos de defeito com `--runxfail` para registrar a falha real.
5. Revisada a solução inicial: duplicados removidos, partição inválida acrescentada, oráculo de `tarifa_anual` corrigido (comprovado por mutação manual temporária, com `tarifas.py` restaurado) e `xfail` restrito a `TypeError`.
6. Abertas as issues [#77](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/77) e [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78) (labels `bug` e `entrega-2`, milestone "Entrega 2"), com a saída do `--runxfail` como evidência; os números foram incluídos no `reason` dos `xfail`.
7. Reexecutada a suíte (`94 passed, 3 xfailed`, 100%); solução final gravada (commit `bb5025b`).
8. Atualizados `docs/relatorios/cobertura_mutacao.md` (seção `TarifaBancaria`), `docs/plano_de_teste.md` (v1.12, seção 6.6) e este AI-LOG.

## Resultado

- **97 casos** em `tests/unit/test_tarifas.py` (antes: 44): **94 aprovados e 3 `xfail`** (`0.77s`).
- Cobertura estrutural todas-arestas de **97% → 100%** (`54` statements, `0` missed, `24` branches, `0` partial); linha 49 coberta.
- **2 defeitos revelados**, abertos como issues: [#77](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/77) (`tarifa_anual` ignora a antiguidade: esperado 288,00, atual sempre 360,00) e [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78) (meia tarifa do pacote premium usa a tarifa da corrente: esperado 25,00, atual 15,00; a confirmar pelo grupo).
- `_tarifa_com_pacote` é código morto (nunca chamado); fica como entrada para a #50 (Sonar), sem issue de bug.
