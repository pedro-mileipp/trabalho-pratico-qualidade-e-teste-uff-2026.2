# Sessão 17 — Testes unitários e cobertura estrutural de `TarifaBancaria` (issue #40)

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielcamposs`) |
| Data | 22/11/2026 |
| Ferramenta | Claude Code (extensão do VS Code), modelo Claude Opus 5.5 (`claude-opus-5-5`) |
| Atividade | Planejar e executar a issue #40: ampliar os testes unitários de `TarifaBancaria` com técnicas funcionais e comprovar cobertura todas-arestas ≥ 80%; abrir issues para os defeitos revelados |
| Artefatos | `tests/unit/test_tarifas.py`; `docs/relatorios/cobertura_mutacao.md` (seção `TarifaBancaria`); `docs/relatorios/evidencias/cobertura/tarifas-*.txt`; `docs/plano_de_teste.md` (v1.12, seção 6.6); issues #77 e #78; este arquivo e o diff `sessao-17-diff-solucao-inicial-final.diff` |
| Commits | `04f2296` (solução inicial, gerada pela IA, sem revisão) · `bb5025b` (solução final, revisada) |

## Contexto

A issue #40 pede: revisar os casos existentes, ampliar com partição de equivalência, valor-limite, tabela de decisão e teste de laços (técnica no id), cobrir a linha 49 (desconto de 20% com antiguidade ≥ 36 meses), registrar os números em `docs/relatorios/cobertura_mutacao.md` e abrir issues de bug para defeitos revelados.

Antes da sessão: 44 casos passando e 97% de cobertura de arestas (linha 49 não coberta).

A IA foi orientada por dois documentos fornecidos pelo responsável: o relatório de issues da Entrega 2 (`relatorio_issues_entrega_2.md`, seção B3 — `TarifaBancaria`) e o enunciado do trabalho (`instrucoes_trabalho.md`), com ênfase no registro do uso de IA.

## Prompts utilizados

Transcrição dos prompts do responsável, na ordem, com o resumo de cada resposta da IA.

**Prompt 1** (com o relatório de issues da Entrega 2 anexado)

> "esse é o plano da entrega, voce deve seguir totalmente esse plano"

**Resposta da IA:** consultou as issues do milestone "Entrega 2" (`gh issue list`) e apontou as diferenças entre o relatório e o GitHub (grupo B dividido em unitários #38–42 e mutação #43–47; Selenium dividido por funcionalidade #56–60; issues já atribuídas). Listou as issues do responsável (#40, #45, #50, #54, #58, #62) e sugeriu começar pela #40.

**Prompt 2**

> "me fale exatamente o que voce vai fazer na #40 qual seu plano de realmente executa-la"

**Resposta da IA:** leu a issue, `app/dominio/tarifas.py`, `tests/unit/test_tarifas.py` e as seções de Pedro e Gabrielle no relatório de cobertura; rodou a cobertura (97%, linha 49) e o `radon cc` (`tarifa_mensal` = 12). Apresentou um plano em 7 etapas e já apontou 3 suspeitas de defeito: `tarifa_anual` sem antiguidade, meia tarifa do pacote premium calculada sobre a corrente e `_tarifa_com_pacote` nunca chamado.

**Prompt 3** (com print da issue #40 no GitHub)

> "tudo isso esta sendo incluido nessa issue?"

**Resposta da IA:** relacionou cada item de "O que fazer" e dos "Critérios de aceite" a uma etapa do plano; explicou que teste de laços não se aplica (a classe não tem laços) e que isso seria justificado no relatório; indicou o que vai além da issue (AI-LOG, Plano de Teste) e o que fica fora (alterar o código de domínio → issues de bug e #50; mutação → #45).

**Prompt 4** (com o enunciado `instrucoes_trabalho.md` e o relatório de issues anexados)

> "voce deve se orientar por 2 arquivos, de enfase para o registro do uso da ia"

**Resposta da IA:** leu o `AI-LOG.md` e a sessão 15 como modelo e propôs o registro: linha na tabela com os 7 campos do enunciado, este arquivo com os prompts transcritos, **commit separado da solução inicial** antes de qualquer revisão, tabela "solução inicial × final", erros da IA e como foram detectados, e atualização da "Configuração do agente".

**Prompt 5**

> "nao entendi o item 1"

**Resposta da IA:** explicou com o exemplo de `tarifa_anual` (corrente, saldo 1000, 36 meses: esperado 288,00, código dá 360,00) o fluxo proposto: teste com o valor correto, que falha (evidência); issue de bug; marcação `xfail(strict=True)` para não bloquear o mutmut da #45. Ofereceu três opções: A (issues + `xfail`), B (só relatório) e C (consultar o grupo antes).

**Prompt 6**

> "faça pelo plano A, como voce planeja seguir com o registro dos prompts e ai-log.md eu preciso que voce siga estritamente isso"

**Resposta da IA:** executou a issue conforme as ações abaixo.

## Solução inicial (gerada pela IA) vs. solução final (após revisão)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações. A solução inicial está no commit `04f2296` e a final no `bb5025b`; o diff entre as duas está em [`sessao-17-diff-solucao-inicial-final.diff`](sessao-17-diff-solucao-inicial-final.diff).

| | Solução inicial (`04f2296`) | Solução final (`bb5025b`) |
|---|---|---|
| Casos | 98 (54 novos) | 97 (53 novos) |
| Resultado | 95 passed, 3 xfailed | 94 passed, 3 xfailed |
| Cobertura de arestas | 100% | 100% |
| Evidência | [`tarifas-1-solucao-inicial.txt`](../../relatorios/evidencias/cobertura/tarifas-1-solucao-inicial.txt) | [`tarifas-2-solucao-final.txt`](../../relatorios/evidencias/cobertura/tarifas-2-solucao-final.txt) |

A solução inicial passou de primeira e já atingia 100%; os problemas abaixo **não apareciam na execução** e só foram encontrados na revisão crítica.

| # | Problema na solução inicial | Como foi identificado | Alteração na solução final |
|---|---|---|---|
| 1 | Casos duplicados: `pe_corrente_saldo_zero` repetia `vl_saldo_zero_sem_sobretaxa`, e `pe_corrente_pacote_antiguidade_nova` repetia `td_r4_corrente_pacote` | Comparação dos parâmetros de cada caso | Os 2 casos `pe_` duplicados foram removidos |
| 2 | Faltava a partição **inválida** de antiguidade (valor negativo) | Revisão das classes de equivalência de `antiguidade_meses` | Acrescentado `pe_antiguidade_negativa_sem_validacao` (−12 meses → 30,00, tratado como conta nova) |
| 3 | `test_tarifa_anual_igual_a_doze_mensais` usava como oráculo `tarifa_mensal(...) * 12`, calculado pelo **próprio código sob teste**: se a mensal estiver errada, a anual erra igual e o teste passa | Mutação manual temporária em `tarifas.py` (`corrente * 0.5` → `corrente * 0.6`, depois revertida): o teste inicial **continuou passando** (`4 passed`) e o final falhou (`assert 216.0 == 180.0`). Evidência: [`tarifas-verificacao-oraculo-anual.txt`](../../relatorios/evidencias/cobertura/tarifas-verificacao-oraculo-anual.txt) | Substituído por `test_tarifa_anual_particao_equivalencia`, com valores explícitos calculados à mão (0; 15 × 12 = 180; 35 × 12 = 420; 38,50 × 12 = 462) |
| 4 | O `xfail` do defeito de `tarifa_anual` aceitava **qualquer** exceção: um erro de digitação no teste também seria aceito como "defeito confirmado" | Execução com `--runxfail`, que mostrou que a falha real é `TypeError: ... unexpected keyword argument 'antiguidade_meses'` | `xfail(strict=True, raises=TypeError, ...)` |
| 5 | `reason` dos `xfail` sem o número da issue | Os números só existiram depois de abrir as issues | `reason="#77: ..."` e `reason="#78: ..."`; comentário do bloco aponta para #77 e #78 |

**Decisão:** a estrutura e os valores esperados da IA foram aceitos (todos conferidos à mão contra o código e a seção 4.3 de `docs/aplicacao.md`); os itens 1–5 foram corrigidos. O código de domínio (`app/dominio/tarifas.py`) **não foi alterado**: correções ficam nas issues #77/#78 e na #50.

**Desvio do plano apresentado:** no prompt 2 a IA propôs reagrupar os 44 casos da Entrega 1 por técnica. Na execução, eles foram mantidos como estavam (só o id `premium_pacote_isencao_5x5` foi renomeado para `premium_pacote_isento_saldo_limite_50000`), para preservar a comparação com a Entrega 1; os prefixos de técnica valem para os casos novos.

## Defeitos revelados

| Issue | Defeito | Evidência (`--runxfail`) |
|---|---|---|
| [#77](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/77) | `tarifa_anual` não recebe nem repassa `antiguidade_meses` (esperado 288,00; sempre 360,00) | `TypeError: TarifaBancaria.tarifa_anual() got an unexpected keyword argument 'antiguidade_meses'` |
| [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78) | meia tarifa do pacote premium usa a tarifa da corrente (esperado 25,00; atual 15,00) — suspeito, a confirmar pelo grupo | `AssertionError: assert 15.0 == 25.0` (2 casos) |

Saída completa: [`tarifas-defeitos-runxfail.txt`](../../relatorios/evidencias/cobertura/tarifas-defeitos-runxfail.txt). As issues foram abertas com labels `bug` e `entrega-2`, milestone "Entrega 2", atribuídas a `danielcamposs`, no formato da #16.

A terceira suspeita (`_tarifa_com_pacote` nunca chamado) não virou issue de bug: é código morto, sem efeito no resultado, e fica como entrada para a #50 (Sonar).

## Ações executadas

1. Criada a branch `test/issue-40-cobertura-tarifas` a partir da `main` atualizada.
2. Medida a situação inicial: `44 passed`, 97% de arestas, linha 49 faltando.
3. Gerada a solução inicial (casos `pe_`, `vl_`, `td_`, `custom_` e 3 casos de defeito com `xfail`), executada e salva em evidência; commit `04f2296` **sem revisão**.
4. Executados os casos de defeito com `--runxfail` para registrar a falha real.
5. Revisão crítica (itens 1–5 da tabela acima), incluindo a mutação manual temporária para comprovar o oráculo fraco; `app/dominio/tarifas.py` restaurado (`git status` limpo em `app/`).
6. Abertas as issues #77 e #78; números incluídos no corpo das issues e no `reason` dos `xfail`.
7. Executada a solução final, salva em evidência; commit `bb5025b`.
8. Atualizados `docs/relatorios/cobertura_mutacao.md`, `docs/plano_de_teste.md` e este AI-LOG.

## Validação

| Verificação | Comando | Resultado |
|---|---|---|
| Cobertura antes | `uv run pytest tests/unit/test_tarifas.py --cov=app.dominio.tarifas --cov-branch --cov-report=term-missing` | `44 passed`; 97% (Missing: 49) |
| Solução inicial | mesmo comando, com `-rxX` | `95 passed, 3 xfailed`; 100% |
| Defeitos | `uv run pytest tests/unit/test_tarifas.py -k defeito --runxfail` | `3 failed` (1 `TypeError`, 2 `AssertionError 15.0 == 25.0`) |
| Oráculo de `tarifa_anual` | mutação manual temporária + teste inicial × final | inicial `4 passed` (não detecta); final `1 failed` (detecta) |
| Solução final | mesmo comando de cobertura, com `-rxX` | `94 passed, 3 xfailed`; **100%** (54 stmts, 24 branches, 0 parciais) |
| Lint | `uv run ruff check tests/unit/test_tarifas.py` | `All checks passed!` |
| Complexidade | `uv run radon cc app/dominio/tarifas.py -s` | `tarifa_mensal - C (12)` (inalterada) |
| Suíte unitária completa | `uv run pytest tests/unit` | `2 failed, 380 passed, 3 xfailed`; as 2 falhas são os bugs #16 e #17 (PIX), já existentes antes desta sessão |
| Valores esperados | conferência manual | ex.: 30 × 0,8 = 24,00; 50 × 0,8 + 5 × 2,50 = 52,50; 30 + 30 × 0,2 + 2,50 = 38,50 |

## Configuração do agente

| Item | Valor |
|---|---|
| Ferramenta | Claude Code, extensão do VS Code (Windows 11) |
| Modelo | Claude Opus 5.5 (`claude-opus-5-5`) |
| Instruções seguidas | `AGENTS.md` do repositório; `relatorio_issues_entrega_2.md` (seção B3); `instrucoes_trabalho.md` (enunciado); memória persistente do agente com duas notas criadas nesta sessão: seguir os dois documentos e registrar o uso de IA no formato do AI-LOG |
| Ferramentas | leitura e edição de arquivos; terminal (Git Bash): `git`, `gh` (issues), `uv run pytest` (+ `pytest-cov`), `uv run ruff`, `uv run radon cc` |
| Ações públicas | abertura das issues #77 e #78, autorizada pelo responsável (prompt 6, plano A); push e PR apenas com autorização |
