# Sessão 6 — Caso de teste manual — PIX (issue #8)

| Campo | Valor |
|---|---|
| Responsável | Alexandre Colmenero (`alexandrelimaxs`) |
| Data | 16/09/2026 |
| Ferramenta | opencode (modelo `opencode-go/deepseek-v4-flash`) |
| Atividade | Projetar e executar caso(s) de teste manual da funcionalidade PIX em `/pix` e documentar |
| Artefatos | `docs/casos_manuais/caso_pix.md` + `docs/casos_manuais/evidencias/` (14 screenshots); link no `README.md`; issue #8 |

## Contexto

A issue #8 pedia projetar e executar caso(s) de teste manual do PIX, com pré-condições, passos, dados de entrada, resultado esperado, resultado obtido e evidência, cobrindo cenários válidos e inválidos (chave inválida, valor inválido, saldo insuficiente etc.), arquivo em `docs/casos_manuais/` e link no README.

## Prompt utilizado

> "Agora eu quero resolver a issue do teste manual atribuido a mim, planeje os passos que preciso realizar no teste manual e pense em um template de documento pra documentar o teste realizado por mim manualmente na interface."

**Resposta da IA:** planejou o fluxo de preparação (subir a app com `DATABASE=/tmp/pix_teste.db`, criar conta, ajustar saldo via `sqlite3` — não há depósito pela UI e a conta nasce com saldo 0) e desenhou 14 casos de teste com partição de equivalência e valor-limite. Depois, com a aprovação do usuário, executou os casos via Selenium (Chrome headless) e documentou.

## Decisões e execução

1. **Preparação:** app rodando com `DATABASE=/tmp/pix_teste.db`; conta `pix@teste.com` criada em `/registro`; saldo ajustado via `sqlite3` (R$ 10.000,00 e R$ 100,00 conforme o caso).
2. **Execução (Selenium + Chrome headless):** 12 casos efetivamente executados na interface (TC-01 a TC-12), com 14 screenshots salvos em `docs/casos_manuais/evidencias/`. Resultado: **11 PASS e 1 FAIL**.
3. **Falha (TC-12):** chave e-mail `a@b@c.com` (dois `@`) foi aceita e o valor debitado — confirma o defeito **#16** (e-mail com dois `@` aceito como válido). Documentada no caso manual com vínculo à issue.
4. **Limitações registradas no documento:**
   - Valor ≤ 0 é barrado pelo HTML5 (`min="0.01"`) antes do backend (TC-05).
   - Limite: execução às 22h (período noturno, R$ 1.000,00) → TC-06 retornou "Operação fora do horário permitido."; o cenário diurno (> R$ 5.000,00) precisa ser executado entre 06h e 20h.
   - Chave bloqueada não é alcançável pela UI na configuração padrão (lista vazia) — coberta por teste unitário.
5. **Documentação:** `docs/casos_manuais/caso_pix.md` preenchido e link adicionado ao `README.md`.

## Validação

- Leituras do corpo HTML das páginas durante a execução confirmaram cada resultado obtido (mensagens flash, saldo e extrato).
- `gh issue view 8` e conferência dos critérios de aceite (caso projetado/executado, arquivo criado, link no README).
- Screenshots em `docs/casos_manuais/evidencias/` conferidos como evidência (presença e tamanho dos arquivos).

## Resultado

- **Artefato principal:** `docs/casos_manuais/caso_pix.md` — 12 casos (11 PASS, 1 FAIL), defeito #16 confirmado e documentado.
- **Evidências:** 14 imagens em `docs/casos_manuais/evidencias/`.
- **Issue #8:** https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/8