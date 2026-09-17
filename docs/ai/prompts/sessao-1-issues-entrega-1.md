# Sessão 1 — Planejamento e criação do milestone e issues da Entrega 1

| Campo | Valor |
|---|---|
| Responsável | Alexandre Colmenero (`alexandrelimaxs`) |
| Data | 16/09/2026 |
| Ferramenta | opencode (modelo `opencode-go/deepseek-v4-flash`) |
| Atividade | Planejamento e criação do milestone e das issues da Entrega 1 |
| Artefatos | Milestone "Entrega 1"; 12 issues; labels |

## Contexto

Planejar o milestone e as issues da **Entrega 1** (Peso 3) do Trabalho Prático de Qualidade e Teste, alinhados ao `docs/descricao_trabalho.md`, e criá-los no GitHub com `gh`.

## Prompts utilizados (em ordem)

### Prompt 1 — Planejamento geral
> "Olá, eu preciso que você planeje o milestone e issues da primeira entrega do trabalho."

**Resposta da IA:** Proposta inicial de milestone "Entrega 1" com um plano amplo de 16 issues (incluía infraestrutura — CI, config do pytest — e atualização do README), além das 5 issues de testes unitários, 5 de casos manuais, TestLink e bug tracking.

**Decisão:** a estrutura serviu de base para discussão, mas não estava alinhada 1:1 com o enunciado — revisada no prompt 2.

**Validação:** comparação com os itens da Entrega 1 em `docs/descricao_trabalho.md`.

### Prompt 2 — Alinhamento exato ao enunciado
> "eu quero que as issues sejam exatamente o que o @docs/descricao_trabalho.md pede na entrega 01"

**Resposta da IA:** Revisão para 13 issues espelhando os itens da Entrega 1: Plano de Teste (com escopo do sistema), 5 issues de testes unitários (uma classe por membro), 5 de casos manuais (uma funcionalidade por membro), TestLink e bug tracking. Removidas as issues de CI/pytest/README (vinham do `docs/plano_projeto.md`, não do enunciado).

**Decisão:** aceito o alinhamento.

**Validação:** conferência item a item com as seções da Entrega 1 do enunciado.

### Prompt 3 — Exclusão do bug tracking das issues
> "deixe de lado o bug tracking, isso será feito manualmente"

**Resposta da IA:** Removida a issue de bug tracking → 12 issues no total.

**Decisão:** aceito; o reporte de erros será feito manualmente pelo grupo (como issues `bug` criadas à medida que defeitos forem encontrados).

**Validação:** contagem final de 12 issues.

### Prompt 4 — Gerar texto explicativo nas issues
> "Sim, e pode gerar um pequeno texto dentro da issue explicando o que deve ser feito."

**Resposta da IA:** Corpos das 12 issues estruturados com as seções **Objetivo**, **O que fazer** e **Critérios de aceite**, descrevendo a API/regras a testar (para unitários e manuais) e o artefato esperado.

**Decisão:** aceito; os textos guiam a execução de cada integrante.

**Validação:** revisão dos textos gerados antes da criação.

### Prompt 5 — Identificar as issues mais complexas
> "quais desses testes unitarios e casos manuais são os mais complexos? quero pegar o mais complexo de cada tipo pra mim"

**Resposta da IA:** Ranking com medição real de complexidade ciclomática via `uv run radon cc app/dominio -s`. Para unitários, recomendou `TransacaoPix` (CC 11 no método `autorizar`, mas com 3 métodos densos — `autorizar`, `solicitar_chargeback`, `_validar_cpf` — e CC 7 na classe). Para manuais, recomendou **PIX** (rota com 6 caminhos de recusa).

**Decisão:** aceito; Alexandre ficou com `TransacaoPix` (unitário) e `PIX` (manual).

**Validação:** saída do `radon cc` conferida para todos os módulos de domínio.

### Prompt 6 — Atribuição das issues
> "Sim" (confirmação para ficar com TransacaoPix e PIX)

**Resposta da IA:** atribuiu as issues #3 (`test: casos unitários — TransacaoPix`) e #8 (`docs: caso de teste manual — PIX`) ao usuário `alexandrelimaxs`.

**Decisão:** aceito; as demais issues permaneceram sem assignee para auto-atribuição dos integrantes.

**Validação:** `gh issue edit 3 --add-assignee alexandrelimaxs` e `gh issue edit 8 --add-assignee alexandrelimaxs` executados com sucesso.

## Ações executadas

1. `gh api repos/.../milestones` → criação do milestone **"Entrega 1"** com due em 21/09/2026 (próxima segunda).
2. `gh label create` → labels `entrega-1`, `teste-unitario`, `teste-manual`, `documentacao`.
3. `gh issue create` → 12 issues com título, corpo explicativo, labels e milestone.
4. `gh issue edit` → assignee em #3 e #8.

## Issues criadas

| # | Título | Labels |
|---|---|---|
| 2 | docs: elaborar Plano de Teste com escopo do sistema | documentacao, entrega-1 |
| 3 | test: casos unitários — TransacaoPix | teste-unitario, entrega-1 |
| 4 | test: casos unitários — CalculadoraJuros | teste-unitario, entrega-1 |
| 5 | test: casos unitários — TarifaBancaria | teste-unitario, entrega-1 |
| 6 | test: casos unitários — SimuladorEmprestimo | teste-unitario, entrega-1 |
| 7 | test: casos unitários — DecisorCredito | teste-unitario, entrega-1 |
| 8 | docs: caso de teste manual — PIX | teste-manual, entrega-1 |
| 9 | docs: caso de teste manual — Auth | teste-manual, entrega-1 |
| 10 | docs: caso de teste manual — Tarifas | teste-manual, entrega-1 |
| 11 | docs: caso de teste manual — Empréstimo | teste-manual, entrega-1 |
| 12 | docs: caso de teste manual — Crédito | teste-manual, entrega-1 |
| 13 | docs: registrar cenário de teste no TestLink | documentacao, entrega-1 |

## Validação geral

- `gh issue list --milestone "Entrega 1"` → 12 issues abertas no milestone.
- `gh api repos/.../issues/{11,12,13}` → campo `milestone.title` = "Entrega 1" confirmado.
- `gh label list` → labels criadas com as cores/descrições definidas.