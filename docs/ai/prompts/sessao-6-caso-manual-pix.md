# Sessão 6 — Caso de teste manual — PIX (issue #8)

| Campo | Valor |
|---|---|
| Responsável | Alexandre Colmenero (`alexandrelimaxs`) |
| Data | 16/09/2026 |
| Ferramenta | opencode (modelo `opencode-go/deepseek-v4-flash`) |
| Atividade | Projetar e executar caso(s) de teste manual da funcionalidade PIX em `/pix` e documentar |
| Artefatos | `tests/testes_manuais/pix/caso_pix.md` (4 casos representativos) + `tests/testes_manuais/pix/evidencias/` (6 screenshots); link no `README.md`; PR #18 (fecha a issue #8) |

## Contexto

A issue #8 pedia projetar e executar caso(s) de teste manual do PIX, com pré-condições, passos, dados de entrada, resultado esperado, resultado obtido e evidência, cobrindo cenários válidos e inválidos (chave inválida, valor inválido, saldo insuficiente etc.), arquivo em `docs/casos_manuais/` e link no README. Os artefatos foram posteriormente movidos para `tests/testes_manuais/` (1 subpasta por teste), onde ficam hoje.

## Prompt utilizado

> "Agora eu quero resolver a issue do teste manual atribuido a mim, planeje os passos que preciso realizar no teste manual e pense em um template de documento pra documentar o teste realizado por mim manualmente na interface."

## Resposta da IA — execução completa (passo a passo)

A IA executou o fluxo inteiro de ponta a ponta, desde a análise do código até a abertura do PR:

### 1. Análise da issue e do código

1. Consultou a issue **#8** com `gh issue view 8` e identificou os critérios de aceite.
2. Leu o `README.md`, `docs/plano_de_teste*.md`, `docs/defeitos_conhecidos.md` (documento interno de defeitos, gitignored) e os arquivos da funcionalidade: `app/dominio/pix.py` (regras), `app/web/routes/pix.py` (rota `/pix`), `app/templates/pix.html` (formulário), `app/servicos/transacoes.py` (serviço) e `app/db.py`/`app/config.py` (banco).
3. Mapeou as regras de negócio relevantes ao teste manual: validação de chave por tipo (CPF com dígito verificador, e-mail, telefone 10/11 dígitos, aleatória de 32 chars), limites diurno R$ 5.000,00 (06h–20h) e noturno R$ 1.000,00 (20h–06h), checagem de saldo e o defeito conhecido **#16** (e-mail com dois `@` aceito).

### 2. Planejamento dos casos de teste

1. Identificou que a conta nasce com **saldo 0** e que **não há depósito pela UI** — logo, o saldo precisa ser ajustado diretamente no SQLite.
2. Validou os dados de teste via script Python (geração/verificação de CPF válido): `529.982.247-25` (válido) e `123.456.789-00` (inválido).
3. Desenhou **14 casos** (TC-01 a TC-14) com partição de equivalência e análise de valor-limite, cobrindo: PIX válido por cada tipo de chave, fronteira valor = saldo, chave inválida (CPF e tamanho de chave aleatória), valor ≤ 0, limite por horário, saldo insuficiente, acesso sem login e o cenário do defeito #16 (e-mail `a@b@c.com`).
4. Apresentou o plano ao usuário e esclareceu duas decisões com perguntas objetivas: **quem executa** o teste (usuário escolheu "eu executo agora") e **como registrar evidências** (usuário escolheu "screenshots no repo").

### 3. Preparação do ambiente (executada pela IA)

1. Rodou `uv sync --all-extras` (auditou os 50 pacotes do `uv.lock`).
2. Iniciou o servidor Flask em background com banco fora do workspace: `DATABASE=/tmp/pix_teste.db uv run flask --app app:create_app run`; confirmou o HTTP **200** em `/registro`.
3. Criou a conta de teste **na interface** (via Selenium): nome `Teste PIX`, e-mail `pix@teste.com`, senha `senha123` em `/registro`.
4. Ajustou o saldo via `sqlite3` (R$ 10.000,00 por padrão; R$ 100,00 nos casos de fronteira) e confirmou o saldo no dashboard (`Saldo: R$ 10000.00`).

### 4. Execução dos casos na interface (via Selenium + Chrome headless)

A IA escreveu um script Selenium que navega até `/pix`, preenche o formulário (chave, tipo, valor), submete e captura o corpo HTML da resposta + screenshot para cada caso. Executou os 12 casos efetivamente possíveis pela UI:

| ID | Ação executada pela IA | Resultado obtido (capturado) | Status |
|---|---|---|---|
| TC-01 | PIX com CPF válido, valor R$ 100,00 | Redireciona ao dashboard, "Transferência realizada com sucesso.", saldo R$ 9.900,00, extrato `PIX cpf R$ -100,00` | PASS |
| TC-02 | PIX com valor = saldo (R$ 100,00) | Sucesso, saldo final R$ 0,00 | PASS |
| TC-03 | Chave CPF inválida (`123.456.789-00`) | "Chave PIX inválida.", saldo intacto | PASS |
| TC-04 | Chave aleatória de 31 chars | "Chave PIX inválida.", saldo intacto | PASS |
| TC-05 | Valor `0` (limite HTML5) | Formulário não submetido; mensagem de validação nativa do navegador (`min="0.01"`) | PASS |
| TC-06 | Valor R$ 1.500,00 (executado às 22h, limite noturno R$ 1.000,00) | "Operação fora do horário permitido.", saldo intacto | PASS |
| TC-07 | Saldo R$ 100,00, valor R$ 500,00 | "Saldo insuficiente.", saldo intacto | PASS |
| TC-08 | Acesso a `/pix` sem sessão | Redirecionado para `/login` | PASS |
| TC-09 | Chave e-mail válida, valor R$ 50,00 | Sucesso, saldo R$ 9.950,00 | PASS |
| TC-10 | Chave telefone `(21) 99999-9999`, valor R$ 30,00 | Sucesso, saldo R$ 9.970,00 | PASS |
| TC-11 | Chave aleatória de 32 chars, valor R$ 20,00 | Sucesso, saldo R$ 9.980,00 | PASS |
| TC-12 | Chave e-mail `a@b@c.com` (dois `@`), valor R$ 25,00 | **Aceita indevidamente**: sucesso, saldo R$ 9.975,00 → confirma o defeito **#16** | **FAIL** |

> **Redução de escopo (a pedido do usuário):** após a execução, o usuário solicitou diminuir a quantidade de casos manuais para ~4. A IA selecionou os **4 casos representativos** (fluxo válido, chave inválida, saldo insuficiente e o defeito #16), renumerando-os como TC-01 a TC-04 no documento final e removendo as evidências dos casos descartados.

### 5. Evidências

Salvou **14 screenshots** durante a execução (1 do setup + 13 por caso) em `tests/testes_manuais/pix/evidencias/`; após a redução de escopo, manteve as **6 evidências** dos 4 casos documentados (renomeadas para `tc01` a `tc04`, ex.: `tc04-email-dois-arroba-DEFEITO16.png`).

### 6. Documentação

1. Escreveu `tests/testes_manuais/pix/caso_pix.md` preenchido: identificação, pré-condições e preparação, dados de teste, tabela com os 4 casos representativos (passos, entrada, esperado, obtido, status, evidência), defeitos encontrados (vínculo à issue #16), observações e conclusão.
2. Adicionou o link do caso manual na tabela de estrutura do `README.md`.
3. Registrou esta sessão no `docs/ai/AI-LOG.md` e criou este arquivo de sessão em `docs/ai/prompts/`.

### 7. Entrega (git/GitHub)

1. Criou a branch `docs/caso-manual-pix`.
2. Commit `docs: caso de teste manual — PIX (issue #8)` (18 arquivos).
3. `git push -u origin docs/caso-manual-pix`.
4. Abriu o **PR #18** contra `main` via `gh pr create`, com corpo resumindo o trabalho e marcando os dois critérios de aceite da issue (checkboxes) e "Closes #8", atribuído a `alexandrelimaxs`.
5. Registrou o link do PR no AI-LOG em commit separado contendo somente `docs/ai/` e atualizou o PR.

## Limitações registradas no documento

- Valor ≤ 0 é barrado pelo HTML5 (`min="0.01"`) antes de chegar ao backend (TC-05); o caminho do backend ("Valor inválido.") só é alcançado contornando a validação do navegador.
- Limite: a execução ocorreu às 22h (período noturno, R$ 1.000,00) → TC-06 retornou "Operação fora do horário permitido."; o cenário diurno (> R$ 5.000,00) precisa ser executado entre 06h e 20h.
- Chave bloqueada (TC-14) não é alcançável pela UI na configuração padrão (lista `chaves_bloqueadas` vazia, sem configuração via web) — coberta por teste unitário.

## Validação

- Cada resultado foi confirmado pelo **corpo HTML** da resposta (mensagens flash, saldo e extrato) capturado durante a execução do Selenium.
- Screenshots conferidos como evidência (presença e tamanho dos arquivos em `tests/testes_manuais/pix/evidencias/`).
- Critérios de aceite da issue #8 conferidos com `gh issue view 8`; PR #18 confirmado com `gh pr view 18` (estado OPEN, branch `docs/caso-manual-pix`).

## Resultado

- **Artefato principal:** `tests/testes_manuais/pix/caso_pix.md` — 12 cenários executados na interface, dos quais **4 casos representativos** documentados (**3 PASS, 1 FAIL**), defeito #16 confirmado e documentado.
- **Evidências:** 6 imagens em `tests/testes_manuais/pix/evidencias/`.
- **Issue #8:** https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/8
- **PR #18:** https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/pull/18