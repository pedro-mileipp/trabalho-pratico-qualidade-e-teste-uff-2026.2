# Sessão 25 — Plano e execução dos testes de PIX (issues #38, #43, #48, #56 e #64)

| Campo | Valor |
|---|---|
| Responsável | Alexandre Colmenero (`alexandrelimaxs`) |
| Data | 22/11/2026 |
| Ferramenta | opencode (CLI) |
| Modelos | `opencode-go/deepseek-v4.1-flash` (implementação) e `opencode-go/deepseek-v4-pro` (revisão independente do plano e do repositório, solicitada pelo responsável) |
| Atividade | Plano de Teste global + planejamento do PIX; testes unitários e cobertura estrutural; mutação; inspeção Sonar; testes de sistema Selenium; atualização de README/AGENTS (issues #38, #43, #48, #56 e #64) |
| Artefatos | `docs/plano_de_teste.md` (v1.19–v1.23), `tests/unit/test_pix.py`, `tests/system/pix/`, `tests/system/conftest.py`, `app/templates/pix.html`, `app/web/routes/pix.py`, `docs/relatorios/cobertura_mutacao.md`, `docs/relatorios/inspecao_sonar.md`, `README.md`, `AGENTS.md` |

## Contexto

Linha de base: **638 passed, 3 xfailed** (os `xfail` eram o defeito #78, de Tarifas). O Plano de Teste estava na versão 1.18, sem seção de PIX, e ainda afirmava que a suíte tinha 2 falhas de PIX e que a mutação estava bloqueada — informação desatualizada. Os defeitos **#16 e #17 já estavam corrigidos** no commit `e7881bd` (PR #89), mas as issues seguiam abertas e sem evidência de antes/depois.

Objetivo da sessão: **planejar antes de implementar** (o plano de teste como artefato de desenho, não como relatório retroativo), executar as issues #38, #43, #48 e #56 e atualizar a documentação da #64, fechando cada issue com evidência.

Regras definidas pelo responsável:

- o Plano de Teste deveria ser atualizado **antes** da implementação;
- o escopo da atualização seria **global** (não só PIX);
- as correções de Sonar ficariam atreladas à **#48**;
- **uma PR por issue** (sem agrupar);
- **commits curtos**, separados por contexto, mesmo que aumentassem a quantidade;
- a ordem de execução **não** deveria ser refletida em nenhum artefato de documentação;
- o merge do PR final só seria feito após revisão do responsável.

## Prompt/instrução do responsável

Trechos das instruções registradas nesta sessão (o histórico completo da conversa não é versionado):

> “nós temos que ir fechando as issues, porém, devemos atualizar o plano de testes antes de implementar, como se ele fosse um plano de testes”

> “1 - Global; 2 - Sim, essas correções devem ficar atreladas à issue de resolver apontamentos do Sonar, certo?; 3 - Ainda não; 4 - Isso, tem que ser PRs separados; 5 - Isso já foi resolvido.”

> “Siga essa ordem sem refleti-la em nenhum artefato de doc”

> “Ao realizar as mudanças, separe-as em commits curtos e diretos mesmo que isso faça aumentar a quantidade de commits. Não coloque todas as mudanças de contextos diferentes em um só commit.”

> “16 e 17 já foram resolvidas? Você pode associar a issue ao PR que fez esse commit por favor e atualizar o status da issue?”

> “Eu mudei o modelo de IA para o Pro. Revise esse plano e todo o repositório pra ver se há algum ponto faltando ou algo a ser corrigido.”

> “sobre o PR 6, nao faça o merge sem minha revisao” → depois: “Revisei e pode fazer merge”

## Decisões da IA e revisão do responsável

| Momento | Decisão/proposta da IA | Revisão do responsável | Resultado |
|---|---|---|---|
| Plano | Atualizar o Plano de Teste **global** e criar a seção 6.10.1 com o desenho dos testes **antes** de codar | Aprovou o escopo global e o princípio “plano primeiro” | Seção 6.10.1 (técnicas, casos planejados, dados, oráculos, critérios, riscos) |
| Defeitos #16/#17 | Não refazer a correção (já presente em `e7881bd`); comprovar antes/depois, ajustar a documentação e fechar | Confirmou que já estavam resolvidas e pediu associar as issues ao PR que fez o commit | Issues fechadas com comentário de resolução e cross-reference com a PR #89 |
| Sonar | A classe `pix.py` tem 0 apontamentos; corrigir também `routes/pix.py` e `pix.html` (7 no total) | Perguntou se as correções ficariam atreladas à #48; a IA confirmou e o responsável aprovou | 7 → 0 apontamentos de PIX; PR #94 |
| Processo | Agrupar as mudanças em uma única PR | Exigiu **PRs separadas** | PRs #91–#96 |
| Commits | Commits por issue | Exigiu commits **curtos e por contexto** | Ex.: 8 commits no PR #91; 3 no #48 |
| Documentação | Registrar a ordem de execução no Plano | Proibiu refletir a ordem em artefato de doc | Seção 6.10 sem cronograma/roadmap de execução |
| Sistema | Usar limites diurno/noturno nos testes de sistema | Aprovou o plano com a ressalva de determinismo; a IA removeu cenários dependentes de horário | 6 cenários determinísticos; 55 passed + 1 xfail na suíte de sistema |
| Mutação | Aceitar 4 sobreviventes como equivalentes, com justificativa | **Revisão de fechamento** (tabela abaixo) | `pix-execucao-2-depois.txt` |
| Fechamento | Mergear o PR #96 | “não faça o merge sem minha revisão” → “Revisei e pode fazer merge” | PR #96 mergeado pelo responsável |

## Revisão independente solicitada (modelo Pro)

Depois da primeira rodada, o responsável trocou o modelo para `deepseek-v4-pro` e pediu uma revisão do plano e de todo o repositório. A revisão encontrou pontos que a primeira rodada não tinha visto e que foram corrigidos:

1. a instância local do SonarQube estava com a análise de 11/11 (estado “antes”); era preciso re-escanear a `main` atual para o “depois”;
2. a funcionalidade PIX tinha **7** apontamentos (não 6): além dos 6 do template, havia 1 `python:S1192` em `routes/pix.py`;
3. `docs/relatorios/inspecao_sonar.md` tinha **duas seções “6.2”** (Empréstimo e Juros); Juros passou a 6.3, Tarifas a 6.4 e PIX entrou como 6.5;
4. `docs/relatorios/cobertura_mutacao.md` ainda dizia que a mutação estava bloqueada pelas falhas de PIX/Juros;
5. o Plano listava #16/#17 como defeitos abertos e tinha versões 1.14/1.16 duplicadas no registro de mudanças;
6. `docs/aplicacao.md` §4.1 não descrevia as regras corrigidas (e-mail com um único `@`; chargeback de chave bloqueada);
7. o README não tinha as pastas de sistema de Auth, Tarifas e PIX;
8. o AGENTS.md ainda descrevia apenas testes unitários e manuais;
9. `docs/plano_projeto.md` mostrava `app/web/templates/`, CI inexistente e `iso25010.md` pendente;
10. havia um artefato local `md-to-pdf.css` não rastreado.

Essas correções entraram no PR #91 (documentação global) e nos PRs seguintes, conforme o contexto.

## Solução inicial (gerada pela IA) vs. solução final (após revisão)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações. Nos testes unitários, a solução inicial foi gravada antes da revisão da mutação (merge `5cddd5e`, PR #92) e a final depois da triagem (merge `5cd5645`, PR #93). O diff está em [`sessao-25-diff-test-pix-inicial-final.diff`](sessao-25-diff-test-pix-inicial-final.diff).

| Artefato | Solução inicial | Solução final | Alterações realizadas |
|---|---|---|---|
| `tests/unit/test_pix.py` | Merge `5cddd5e`: 104 casos (68 da Entrega 1 + 36 novos), 100% de cobertura; mutação em 91,9% (136/148) | Merge `5cd5645`: **111 casos**, 100% de cobertura; mutação em **97,3%** (144/148) | 7 casos para matar 8 mutantes: valor 1,00; chargeback de 1,00; 7 dias com valor acima do teto; janela noturna com início == fim; CPF que falha só no 1º DV (`52998224733`); CPF válido com DV 0 (`47824504000`) |
| `tests/system/pix/` | Plano inicial previa cenários de limite diurno/noturno | Merge `3a095cf`: 6 cenários sem dependência de horário | Limites de horário ficaram nos unitários; saldo definido pela fixture `definir_saldo_sistema`; seletores por `id` (incluídos na #48) |
| `docs/plano_de_teste.md` | v1.19 (planejamento global + 6.10.1) | v1.23 (resultados 6.10.2–6.10.5) | Estado atual, ferramentas, critérios e resultados por issue |

**Decisão:** a solução inicial foi aceita na estrutura (técnicas, casos e oráculos). A revisão da mutação acrescentou os 7 casos acima; os 4 sobreviventes restantes foram classificados como equivalentes, com justificativa no relatório.

## Validação

| Verificação | Comando | Resultado |
|---|---|---|
| Unitários de PIX | `uv run pytest tests/unit/test_pix.py -q` | 111 passed |
| Cobertura estrutural | `uv run pytest tests/unit/test_pix.py --cov=app.dominio.pix --cov-branch --cov-report=term-missing` | 100% (101 statements, 50 branches) |
| Mutação | `uv run mutmut run` (isolado em `pix.py`) | 148 mutantes, 144 mortos (97,3%); 4 equivalentes |
| Sonar | `./scripts/sonar_local.sh scan` | 26 → 19 apontamentos abertos no projeto; PIX 7 → 0 |
| Sistema PIX | `uv run pytest tests/system/pix -q` | 6 passed |
| Suíte de sistema | `uv run pytest tests/system -q` (duas execuções) | 55 passed, 1 xfailed (40,40s e 43,11s) |
| Suíte completa | `uv run pytest -q` | 705 passed, 4 xfailed |
| Lint / CC | `uv run ruff check app/` · `uv run radon cc app/dominio/pix.py -s` | ruff ok; `autorizar` CC 11 e `solicitar_chargeback` CC 10 |

Evidências: [`cobertura/pix-cobertura.txt`](../../relatorios/evidencias/cobertura/pix-cobertura.txt), [`mutacao/pix-execucao-1-antes.txt`](../../relatorios/evidencias/mutacao/pix-execucao-1-antes.txt), [`mutacao/pix-execucao-2-depois.txt`](../../relatorios/evidencias/mutacao/pix-execucao-2-depois.txt), [`sonar/depois/pix/`](../../relatorios/evidencias/sonar/depois/pix/) e `tests/system/pix/evidencias/`.

## Revisão de fechamento dos PRs (preencher após a conferência)

Esta tabela é o registro da revisão de fechamento feita pelo responsável **após o merge**. Para cada PR, execute a verificação, registre o resultado e a decisão.

| PR | Verificação realizada | Resultado | Data/hora | Decisão |
|---|---|---|---|---|
| #91 — Plano global | Ler a seção 6.10.1 e conferir que não há ordem de execução no documento; conferir o registro de mudanças (v1.19) | a preencher | a preencher | a preencher |
| #92 — Unitários/cobertura | Conferir os 104 casos, os ids de técnica e as regressões #16/#17; rodar `uv run pytest tests/unit/test_pix.py -q` | a preencher | a preencher | a preencher |
| #93 — Mutação | Ler o diff dos 7 casos, o mapeamento mutante → teste e a justificativa dos 4 equivalentes | a preencher | a preencher | a preencher |
| #94 — Sonar | Conferir o diff de `pix.html` e `routes/pix.py`; conferir no JSON 0 abertos e 7 resolvidos; verificar CC | a preencher | a preencher | a preencher |
| #95 — Sistema | Ler os 6 cenários e o page object; rodar `uv run pytest tests/system/pix -q` | a preencher | a preencher | a preencher |
| #96 — README/AGENTS | Conferir os links e o estado atual descrito; verificar que o PR não fecha a #64 | a preencher | a preencher | a preencher |

Comandos de apoio:

```bash
git show 2262858 --stat   # #91
git show 5cddd5e --stat   # #92
git show 5cd5645 --stat   # #93
git show 23b2c86 --stat   # #94
git show 3a095cf --stat   # #95
git show 85abde0 --stat   # #96
```

## Ações executadas

1. `git pull` e linha de base: 638 passed, 3 xfailed; conferência de que #16/#17 já estavam corrigidos em `e7881bd`.
2. PR #91: plano global (escopo, estado atual, ferramentas, critérios, termos), planejamento 6.10.1, correções de documentação e `.gitignore`.
3. PR #92: 36 casos novos, técnicas `pe_`/`vl_`/`td_`/`laco_`/`custom_`, evidência de cobertura, seção `TransacaoPix` no relatório de cobertura/mutação.
4. PR #93: execução 1 (91,9%), triagem dos 12 sobreviventes, 7 casos novos, execução 2 (97,3%), mapeamento mutante → teste e justificativa dos 4 equivalentes.
5. PR #94: correção de 7 apontamentos do Sonar (template + rota), reprodução do “antes” e “depois” na instância local, evidências JSON/log/print, seção 6.5 do relatório de inspeção.
6. PR #95: page object de PIX, 6 cenários Selenium, fixture `banco_sistema`/`definir_saldo_sistema`, evidências e suíte determinística.
7. PR #96: README e AGENTS atualizados; PR deixado aberto para revisão do responsável e mergeado após a aprovação.

## Resultado

- **Plano**: seção 6.10.1 escrita antes da implementação, sem ordem de execução; documentação global alinhada ao estado real (v1.19–v1.23).
- **Unitários**: 111 casos, 100% de cobertura de arestas.
- **Mutação**: 148 mutantes, 144 mortos (97,3%; 100% descontando 4 equivalentes).
- **Sonar**: 7 → 0 apontamentos na funcionalidade PIX; classe com 0 e CC preservada.
- **Sistema**: 6 cenários de PIX; suíte total 55 passed + 1 xfail, determinística.
- **Suíte completa**: 705 passed, 4 xfailed.
- **Issues fechadas**: #38, #43, #48 e #56 (e #16/#17, já resolvidas). A #64 segue aberta por depender dos slides e dos artefatos de #62/#63.

## Avaliação crítica e lições aprendidas

- **Erro da IA corrigido pela revisão**: a primeira leitura do Sonar considerou só os 6 apontamentos do template; o re-scan mostrou também 1 `S1192` na rota. A revisão independente (modelo Pro) foi o que levantou o ponto.
- **Cache do mutmut**: a primeira re-execução reaproveitou o cache e não rodou os testes novos; foi necessário remover `.mutmut-cache`/`mutants` para medir de verdade. Sem isso, o escore final teria sido reportado errado.
- **Erro da IA pego pelos testes**: um caso novo de chargeback customizado usou `limite_chargeback_dias=15` esperando o teto de valor de 100; o teste falhou e o caso foi corrigido para configurar também `limite_padrao=100`. O erro foi registrado, não escondido.
- **Cobertura 100% não bastava**: os mutantes revelaram fronteiras não testadas (valor 1,00; 7 dias com valor alto; janela com início == fim; `resto == 10` do CPF), o que reforça a diferença entre cobertura estrutural e teste baseado em defeitos.
- **Decisão de escopo**: os testes de sistema não cobrem limites de horário (ficam nos unitários) para não depender do relógio; o saldo é preparado no SQLite porque a interface não tem depósito.

## Configuração do agente

| Item | Valor |
|---|---|
| Ferramenta | opencode (CLI) |
| Modelo | `opencode-go/deepseek-v4.1-flash` (implementação) e `opencode-go/deepseek-v4-pro` (revisão) |
| Instruções de projeto | `AGENTS.md` (uv, camadas, convenções, não criar testes sem solicitação) + diretrizes desta sessão (plano antes da implementação, PRs separadas, commits curtos, ordem fora dos docs) |
| Ferramentas utilizadas | `uv run pytest` (+ `pytest-cov`), `uv run mutmut`, `uv run ruff`, `uv run radon`, `sonar-scanner` + SonarQube local (Docker), Selenium/Chrome headless, `git`, `gh` |
| Escopo da sessão | Plano de Teste da Entrega 2, `TransacaoPix` (unitários, cobertura, mutação, Sonar), testes de sistema de PIX e atualização de README/AGENTS |
