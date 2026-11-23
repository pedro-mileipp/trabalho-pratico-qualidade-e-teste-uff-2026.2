# Sessão 27 — Plano e execução dos testes de PIX (issues #38, #43, #48, #56 e #64)

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

Objetivo: **planejar antes de implementar**, executar as issues #38, #43, #48 e #56 e atualizar a documentação da #64, fechando cada issue com evidência.

## Conversa

### Turno 1 — ler o repositório e planejar antes de implementar

**Prompt (resumo):** ler as docs para contexto; atualizar o Plano de Teste antes de implementar, como um plano de testes de verdade.

**Retorno da IA:** leu `docs/plano_de_teste.md`, `docs/plano_projeto.md`, o enunciado, `docs/aplicacao.md`, os relatórios de cobertura/mutação, Sonar e RNF, o README, o AGENTS e as issues. Constatou:

- suíte verde (638 passed, 3 xfailed), mas o plano dizia que havia 2 falhas de PIX;
- #16 e #17 já corrigidos em `e7881bd` (PR #89), com testes passando;
- o plano não tinha seção de PIX, o relatório de mutação não tinha `TransacaoPix` e o Sonar local estava com a análise de 11/11;
- propôs: atualizar o Plano global + criar a seção 6.10.1 (desenho dos testes) **antes** de codar; depois executar #38, #43, #48 e #56; fechar cada issue com evidência.

**Decisão do responsável:** aceitou o princípio “plano primeiro” e pediu que o escopo da atualização fosse global, não só PIX. Definiu também as regras de processo que valeram para toda a sessão.

**Mensagem do responsável:**

> “leia as docs desse repositorio pra contexto
>
> nós temos que ir fechando as issues, porém, devemos atualizar o plano de testes antes de implementar, como se ele fosse um plano de testes, entende?”

---

### Turno 2 — confirmar #16/#17 e fechar as decisões de escopo

**Prompt (resumo):** confirmar se #16/#17 já estavam resolvidas, vinculá-las ao PR do commit e fechar as decisões pendentes do plano.

**Retorno da IA:** verificou que **#16 e #17 já estavam CLOSED** (motivo `COMPLETED`), com comentário de resolução apontando o commit `e7881bd` e a **PR #89**; o timeline da PR #89 mostra cross-reference para as duas issues. Ajustou o plano conforme as respostas:

- escopo **global** da atualização do Plano de Teste;
- correções de Sonar atreladas à **#48**;
- **uma PR por issue**;
- commits **curtos e por contexto**;
- a ordem de execução **não** seria refletida em nenhum documento.

**Decisão do responsável:** aprovou o plano ajustado e, em seguida, trocou o modelo para o Pro para uma revisão independente do plano e do repositório.

**Mensagem do responsável:**

> “16 e 17 já foram resolvidas? Você pode associar a issue ao PR que fez esse commit por favor e atualizar o status da issue?
>
> 1 - Global
> 2 - Sim, essas correcoes devem ficar atreladas a issue de resolver apontamentos do Sonar, certo?
> 3 - Ainda não.
> 4 - Isso, tem que ser PR's separados.
> 5 - Isso ja foi resolvido.
>
> Siga essa ordem sem refleti-la em nenhum artefato de doc:
> Ao realizar as mudanças, separe-as em commits curtos e diretos mesmo que isso faça aumentar a quantidade de commits.
> Não coloque todas as mudanças de contextos diferentes em um só commit, separe-os pra ficar mais organizado.”

---

### Turno 3 — revisão independente com o modelo Pro

**Prompt (resumo):** revisar o plano e todo o repositório para encontrar pontos faltando ou errados.

**Retorno da IA:** a revisão encontrou 11 pontos que a primeira rodada não tinha visto, entre eles:

1. a instância local do SonarQube estava no estado “antes” (11/11) — era preciso re-escanear a `main` atual;
2. a funcionalidade PIX tinha **7** apontamentos (6 no template + 1 `S1192` em `routes/pix.py`), não 6;
3. `inspecao_sonar.md` tinha **duas seções “6.2”** (Empréstimo e Juros);
4. `cobertura_mutacao.md` ainda dizia que a mutação estava bloqueada;
5. o Plano listava #16/#17 como abertos e tinha versões 1.14/1.16 duplicadas;
6. `aplicacao.md` §4.1 não descrevia as regras corrigidas de PIX;
7. README sem as pastas de sistema de Auth, Tarifas e PIX;
8. AGENTS.md desatualizado;
9. `plano_projeto.md` com `app/web/templates/` e CI inexistente;
10. `iso25010.md` ainda pendente;
11. artefato local `md-to-pdf.css` não rastreado.

**Decisão do responsável:** aceitou as correções e respondeu às quatro decisões pendentes: renumerar as seções, incluir a higiene do `plano_projeto.md`, ignorar `md-to-pdf.css` (mantendo `package-lock.json`) e usar o markdown como base (sem espelhar no Google Docs).

**Mensagem do responsável:**

> “1 - Sim.
> 2 - Sim.
> 3 - Apenas ignore o primeiro.
> 4 - A base é o markdown.”

---

### Turno 4 — executar as issues em PRs separadas

**Prompt (resumo):** aprovação para prosseguir com a implementação.

**Retorno da IA:** executou as mudanças em PRs separadas, com commits curtos por contexto:

- **PR #91** — plano global + seção 6.10.1, correções de documentação e `.gitignore`;
- **PR #92** — 36 casos unitários novos (104 no total), técnicas `pe_`/`vl_`/`td_`/`laco_`/`custom_`, cobertura 100%;
- **PR #93** — mutação: 91,9% na 1ª execução, triagem de 12 sobreviventes, 7 casos novos, **97,3%** na 2ª (100% descontando 4 equivalentes);
- **PR #94** — Sonar: 7 → 0 apontamentos de PIX (template + rota), com reprodução do “antes” e “depois”;
- **PR #95** — 6 cenários Selenium de PIX, fixture `banco_sistema`/`definir_saldo_sistema`, suíte de sistema 55 passed + 1 xfail;
- **PR #96** — README e AGENTS atualizados, deixado aberto para revisão.

No caminho, a IA registrou e corrigiu erros próprios: o cache do mutmut não rodou os testes novos (foi preciso limpar `.mutmut-cache`), um caso de chargeback customizado usou a configuração errada de limite e o Sonar local estava desatualizado.

**Decisão do responsável:** acompanhou a execução e, antes do merge da PR final, exigiu revisão própria.

**Mensagem do responsável:**

> “Pode prosseguir. […]”

> “sobre o PR 6, nao faça o merge sem minha revisao”

---

### Turno 5 — revisar o PR final e autorizar o merge

**Prompt (resumo):** revisão do PR #96 antes do merge.

**Retorno da IA:** manteve o PR #96 aberto, com o resumo do estado: README com as cinco pastas de sistema e as evidências de PIX; AGENTS com os quatro níveis de teste e a suíte em 705 passed + 4 xfailed; Plano com as pendências restantes (#62 e #63); a #64 continuaria aberta por causa dos slides.

**Decisão do responsável:** revisou o PR #96 e autorizou o merge. Em seguida, pediu a atribuição das PRs ao próprio usuário.

**Mensagem do responsável:**

> “Revisei e pode fazer merge”

---

### Turno 6 — atribuir as PRs ao responsável

**Prompt (resumo):** corrigir a autoria/atribuição das PRs abertas.

**Retorno da IA:** atribuiu as PRs #91–#96 ao usuário `alexandrelimaxs` e confirmou a atribuição.

**Decisão do responsável:** aceitou a atribuição.

**Mensagem do responsável:**

> “uma correcao, faça o assing dos pr que que abriu pro meu usuario, por favor”

---

## Solução inicial (gerada pela IA) vs. solução final (após revisão)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações. Nos testes unitários, a solução inicial foi gravada antes da revisão da mutação (merge `5cddd5e`, PR #92) e a final depois da triagem (merge `5cd5645`, PR #93). O diff está em [`sessao-27-diff-test-pix-inicial-final.diff`](sessao-27-diff-test-pix-inicial-final.diff).

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
