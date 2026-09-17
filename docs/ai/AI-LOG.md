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

## Configuração do agente

Conforme o enunciado, registram-se as instruções/ferramentas/configurações do agente usado nesta sessão:

| Item | Valor |
|---|---|
| Ferramenta | opencode (CLI) |
| Modelo | `opencode-go/deepseek-v4-flash` |
| Repositório | `pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2` |
| Instruções de projeto | `AGENTS.md` (padrões: uv, camadas, convenções de commit, não criar testes sem solicitação) |
| Ferramentas utilizadas | `gh` (issues, milestones, labels), `gh api`, `uv run radon cc` (medição de complexidade), edição de arquivos |
| Escopo da sessão | Planejamento/criação de milestone e issues da Entrega 1; documentação do Plano de Teste |

> Nenhuma interação desta sessão envolveu geração ou melhoria de **testes**, portanto não se aplica a exigência de preservar a solução inicial vs. final dos casos de teste.

## Sessões detalhadas

- [Sessão 1 — Planejamento e criação do milestone e issues da Entrega 1](prompts/sessao-1-issues-entrega-1.md)
- [Sessão 2 — Documentação: Plano de Teste e referências](prompts/sessao-2-documentacao-plano-de-teste.md)
- [Sessão 3 — Criação do PR de documentação](prompts/sessao-3-pr-documentacao.md)