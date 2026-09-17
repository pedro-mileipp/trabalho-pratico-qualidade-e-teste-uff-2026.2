# AI-LOG — Registro de uso de IA

Registro das interações com ferramentas de IA Generativa que contribuíram substancialmente para os artefatos do trabalho, conforme `docs/descricao_trabalho.md`.

> **Como preencher:** cada uso relevante deve ser registrado na tabela abaixo e detalhado em um arquivo próprio dentro de `docs/ai/prompts/`. O campo **Prompt/instrução** referencia o arquivo com a transcrição/descrição da sessão.

## Registro de interações

| Responsável | Atividade | Ferramenta | Prompt/instrução | Resultado | Decisão | Validação |
|---|---|---|---|---|---|---|
| Alexandre Colmenero | Criação do milestone e das issues da Entrega 1 | opencode (modelo `opencode-go/deepseek-v4-flash`) | [Sessão 1 — prompts](prompts/sessao-1-issues-entrega-1.md) | Milestone "Entrega 1" (due 21/09/2026) criado via API; 12 issues 1:1 com os itens da Entrega 1, com labels (`entrega-1`, `teste-unitario`, `teste-manual`, `documentacao`) e corpo explicativo (Objetivo / O que fazer / Critérios de aceite) | Aceitas; bug tracking ficou fora (feito manualmente); issues #3 (TransacaoPix) e #8 (PIX) atribuídas a Alexandre; demais sem assignee para auto-atribuição | `gh issue list --milestone "Entrega 1"` e consulta via `gh api` confirmaram as 12 issues vinculadas ao milestone; labels conferidos via `gh label list` |
| Alexandre Colmenero | Criação do template de Plano de Teste | opencode (modelo `opencode-go/deepseek-v4-flash`) | [Sessão 2 — prompts](prompts/sessao-2-documentacao-plano-de-teste.md) | Criados `docs/plano_de_teste.md` (template em branco) e `docs/plano_de_teste_exemplo.md` (exemplo preenchido, referência) | Aceitos integralmente; exemplo mantido apenas como referência, template em branco fica para o grupo preencher | Revisão do conteúdo gerado nos arquivos; conferência das seções do template |
| Alexandre Colmenero | Atualização das referências nas docs | opencode (modelo `opencode-go/deepseek-v4-flash`) | [Sessão 2 — prompts](prompts/sessao-2-documentacao-plano-de-teste.md) | `README.md` com link e linha na tabela "Estrutura do Repositório" para `docs/plano_de_teste.md` e `docs/plano_de_teste_exemplo.md`; `docs/aplicacao.md` com o arquivo na árvore de diretórios | Aceito | Leitura dos arquivos após as edições; links relativos conferidos |
| Alexandre Colmenero | Criação de branch e PR de documentação | opencode (modelo `opencode-go/deepseek-v4-flash`) | [Sessão 3 — prompts](prompts/sessao-3-pr-documentacao.md) | Branch `docs/atualizacao-documentacao`; commit `3834c5e` com os 7 arquivos de documentação; **PR #14** criado contra `main` com descrição resumida e atribuído a `alexandrelimaxs` | Aceito; PR agrupa apenas documentação; registro do PR no AI-LOG feito em commit separado contendo somente `docs/ai/` | Link do PR #14 conferido; `git log` e `git status -sb` confirmaram commit e sincronização com `origin` |
| Alexandre Colmenero | Testes unitários de `TransacaoPix` (issue #3) | opencode (modelo `opencode-go/deepseek-v4-flash`) | [Sessão 4 — prompts](prompts/sessao-4-testes-unitarios-pix.md) | `tests/unit/test_pix.py` com 68 casos parametrizados (partição de equivalência, valor-limite e tabela de decisão); config pytest em `pyproject.toml`; resultado **66 passam, 2 falham** revelando os defeitos conhecidos #1 (e-mail com dois `@`) e #2 (chave bloqueada ignora valor na faixa de dias) | Aceito; solução inicial afirmava o comportamento bugado nos 2 casos de defeito — revisado para esperar o comportamento correto, tornando as falhas a evidência dos defeitos; correção fica para a Entrega 2 | `uv run pytest tests/unit/test_pix.py` (2 failed, 66 passed) e `uv run ruff check tests/unit/test_pix.py` (ok); solução inicial vs. final documentada na sessão |
| Alexandre Colmenero | Issues de defeitos, atualização do PR #15 e merge | opencode (modelo `opencode-go/deepseek-v4-flash`) | [Sessão 5 — prompts](prompts/sessao-5-issues-defeitos-merge.md) | Milestone "Entrega 2" e label `entrega-2` criados; issues **#16** e **#17** abertas (uma por defeito), atribuídas a `alexandrelimaxs` com labels `bug`/`entrega-2`; PR #15 atualizado referenciando as issues e mergeado contra `main` (fecha #3) | Aceito; cada issue documenta evidência do teste que falha, esperado vs. atual e correção prevista para a Entrega 2 | Conferência via `gh api` das issues (assignee, labels, milestone); `gh pr view 15` antes/depois; merge confirmado pelo estado do PR e `git log` de `main` |
| Alexandre Colmenero | Caso de teste manual — PIX (issue #8) | opencode (modelo `opencode-go/deepseek-v4-flash`) | [Sessão 6 — prompts](prompts/sessao-6-caso-manual-pix.md) | Caso manual do PIX projetado e **executado** via Selenium/Chrome headless: 12 cenários executados na interface, dos quais **4 casos representativos** documentados em `tests/testes_manuais/pix/caso_pix.md` (TC-01 válido, TC-02 chave inválida, TC-03 saldo insuficiente e TC-04 defeito #16) com 6 screenshots em `tests/testes_manuais/pix/evidencias/`; resultado **3 PASS e 1 FAIL** — o FAIL confirma o defeito **#16** (e-mail com dois `@` aceito); artefatos movidos de `docs/casos_manuais/` para `tests/testes_manuais/` (subpasta por teste); descrição do PR #18 com as imagens de evidência anexadas; **PR #18 mergeado contra `main`** (fecha #8) | Aceito; limitações registradas (valor ≤ 0 barrado por HTML5; limite noturno às 22h; chave bloqueada não alcançável via UI); escopo reduzido a 4 casos a pedido do usuário; reorganização e merge realizados | Resultados confirmados pelo corpo HTML das respostas; `gh issue view 8` conferindo os critérios de aceite; arquivos de evidência conferidos na branch remota via `gh api`; merge do PR #18 confirmado |

## Configuração do agente

Conforme o enunciado, registram-se as instruções/ferramentas/configurações do agente usado nesta sessão:

| Item | Valor |
|---|---|
| Ferramenta | opencode (CLI) |
| Modelo | `opencode-go/deepseek-v4-flash` |
| Repositório | `pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2` |
| Instruções de projeto | `AGENTS.md` (padrões: uv, camadas, convenções de commit, não criar testes sem solicitação) |
| Ferramentas utilizadas | `gh` (issues, milestones, labels), `gh api`, `uv run radon cc` (medição de complexidade), `uv run pytest`, `uv run ruff`, edição de arquivos |
| Escopo da sessão | Planejamento/criação de milestone e issues da Entrega 1; documentação do Plano de Teste; testes unitários de `TransacaoPix` (issue #3) |

> Nas sessões 1 a 3 não houve geração ou melhoria de **testes**. Na **Sessão 4** (testes unitários de `TransacaoPix`) a exigência de preservar a solução inicial vs. final se aplica e está documentada no próprio arquivo da sessão.

## Sessões detalhadas

- [Sessão 1 — Planejamento e criação do milestone e issues da Entrega 1](prompts/sessao-1-issues-entrega-1.md)
- [Sessão 2 — Documentação: Plano de Teste e referências](prompts/sessao-2-documentacao-plano-de-teste.md)
- [Sessão 3 — Criação do PR de documentação](prompts/sessao-3-pr-documentacao.md)
- [Sessão 4 — Testes unitários de `TransacaoPix` (issue #3)](prompts/sessao-4-testes-unitarios-pix.md)
- [Sessão 5 — Issues de defeitos, atualização do PR #15 e merge](prompts/sessao-5-issues-defeitos-merge.md)
- [Sessão 6 — Caso de teste manual — PIX (issue #8)](prompts/sessao-6-caso-manual-pix.md)