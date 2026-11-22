# Sessão 23 — Sonar: `CalculadoraJuros` e funcionalidade de autenticação (issue #49)

| Campo | Valor |
|---|---|
| Responsável | Gabrielle Rosa (`n2Gabrielle`) e Daniel Izu (`danielcamposs`), em dupla |
| Data | 22/11/2026 |
| Ferramenta | Claude Code (extensão do VS Code), modelo Claude Opus 5.5 (`claude-opus-5-5`) / SonarQube local no Docker do Ubuntu (WSL 2) / Terminal (`uv run pytest`) |
| Atividade | Issue #49 (da Gabrielle Rosa, feita em dupla com Daniel Izu): verificar os apontamentos do Sonar em `CalculadoraJuros` e corrigir os da funcionalidade de autenticação |
| Artefatos | `app/templates/login.html`, `app/templates/registro.html`, `app/web/routes/auth.py` |

## Contexto

A sessão foi feita em dupla: Gabrielle Rosa (responsável pela issue) e Daniel Izu, juntos, usando o Claude Code na máquina de Daniel. Os prompts abaixo foram digitados por Daniel.

A issue #49 pede resolver os apontamentos do Sonar na `CalculadoraJuros`. A IA verificou que a classe tem **0 apontamentos**, na A2 e na análise atual, e que ela não tem tela nem rota (nenhum arquivo de `app/web` ou `app/templates` a usa). Por isso não há o que corrigir nem na classe nem numa tela da mesma funcionalidade. Os 30 apontamentos restantes no projeto estavam em telas de outras issues (empréstimo #51, PIX #48) e na autenticação, com 12 apontamentos sem responsável.

## Prompt utilizado

> 1. "preciso fazer para a calculadora juros"
> 2. "faça a opção A"

A opção A, proposta pela IA na resposta ao prompt 1, era: registrar na #49 que `CalculadoraJuros` não tem apontamentos (com print) e corrigir os apontamentos da autenticação, como na #52 do Pedro, em que a classe também não tinha apontamentos e foi corrigida a tela da funcionalidade.

**Resposta da IA:** antes de agir, a IA avisou que a #49 está atribuída à Gabrielle; o responsável informou que a issue estava sendo feita em dupla com ela. Levantou na última análise os 12 apontamentos da autenticação: 10 de acessibilidade em `login.html` e `registro.html`, `python:S1192` (literal `"registro.html"` repetido 3 vezes) e `python:S6965` (rota `/logout` sem métodos declarados) em `routes/auth.py`. Antes de mudar o HTML, conferiu que o page object do Selenium de autenticação localiza os campos por `name`, e não por `id`.

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações. A solução inicial foi gravada no commit `07e17ef` **antes de qualquer revisão**; o diff está em [`sessao-23-diff-sonar-auth.diff`](sessao-23-diff-sonar-auth.diff).

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| **Commit `07e17ef`:** `label for`/`id` nos 5 campos de `login.html` e `registro.html`; constante `TEMPLATE_REGISTRO` em `routes/auth.py`; `@bp.route("/logout", methods=["GET"])`. Unitários, integração e segurança: 546 passando (2 falhas de PIX, anteriores); Selenium de autenticação: 12 passando; `ruff` ok | Igual à inicial: a revisão não encontrou alteração necessária no código. SonarQube: autenticação **12 → 0** (`CLOSED`/`FIXED`), projeto 37 → 25, nenhum apontamento novo | Nenhuma no código. A revisão verificou: (1) `/logout` só com `GET` está correto, porque a tela usa um link `<a href>` e os testes usam `GET` — o risco de CSRF de logout foi registrado no relatório como conhecido e de baixo impacto; (2) os `id`s repetidos (`email`, `senha`) ficam em páginas diferentes; (3) a CC da `CalculadoraJuros` não mudou |

**Decisão:** a solução da IA foi aceita sem alterações, depois da revisão e da validação no SonarQube. `CalculadoraJuros` foi registrada como classe sem apontamentos, com justificativa e print. A correção foi feita na autenticação, porque eram os únicos apontamentos sem responsável.

**Validação inicial:** `uv run ruff check app/` → `All checks passed!`; `uv run pytest tests/unit tests/integration tests/rnf -q` → `546 passed` (2 falhas de PIX, #16 e #17, anteriores); `uv run pytest tests/system/auth -q` → `12 passed`. Evidência: [`pytest-solucao-inicial.txt`](../../relatorios/evidencias/sonar/depois/juros-auth/pytest-solucao-inicial.txt).

**Validação final:** SonarQube, no projeto separado `banco-digital-uff-2026-2-issue49`, com o mesmo perfil comprehensive. "Antes" (`main`, `bbabd18`): 37 apontamentos, 12 da autenticação, 0 em `juros.py`. "Depois" (`07e17ef`): 25 apontamentos, 0 da autenticação, 0 em `juros.py`, 12 `CLOSED`/`FIXED`. Evidências: [`antes-main/issues-abertas.json`](../../relatorios/evidencias/sonar/depois/juros-auth/antes-main/issues-abertas.json), [`depois-branch/issues-resolvidas.json`](../../relatorios/evidencias/sonar/depois/juros-auth/depois-branch/issues-resolvidas.json), prints [`issues-juros.png`](../../relatorios/evidencias/sonar/depois/juros-auth/issues-juros.png), [`issues-auth-resolvidos.png`](../../relatorios/evidencias/sonar/depois/juros-auth/issues-auth-resolvidos.png), [`issues-auth-abertos.png`](../../relatorios/evidencias/sonar/depois/juros-auth/issues-auth-abertos.png) e [`dashboard-depois.png`](../../relatorios/evidencias/sonar/depois/juros-auth/dashboard-depois.png).

## Ações executadas

1. Verificados os apontamentos de `juros.py` (0) e as referências à `CalculadoraJuros` na aplicação (nenhuma tela nem rota).
2. Levantados os 30 apontamentos restantes por arquivo e responsável; proposta a opção A (aprovada no prompt 2).
3. Criada a branch `fix/issue-49-sonar-juros-auth`; corrigidos os 12 apontamentos da autenticação; solução gravada sem revisão (`07e17ef`).
4. Revisão: rota de logout, `id`s repetidos, seletores do Selenium e CC da classe; nenhuma alteração necessária.
5. Análises "antes" e "depois" num projeto separado da mesma instância, para não sobrescrever o projeto principal, que o responsável usava nos prints da #50.
6. Prints tirados com o usuário local só de leitura (`prints`).
7. Atualizados `docs/relatorios/inspecao_sonar.md` (seção 6.3), `docs/plano_de_teste.md` (v1.17, seção 6.4) e o AI-LOG.

## Resultado

- `CalculadoraJuros`: **0 apontamentos** no Sonar — justificado (sem tela nem rota), com print.
- Autenticação: **12 → 0** apontamentos (`login.html` 4, `registro.html` 6, `routes/auth.py` 2); projeto **37 → 25** sem apontamentos novos.
- Testes de autenticação (unitários com mock, integração, segurança e Selenium) passando.
