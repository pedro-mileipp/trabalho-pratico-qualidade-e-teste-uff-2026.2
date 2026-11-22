# Sessão 22 — Correção dos apontamentos do Sonar em `TarifaBancaria` (issue #50)

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielcamposs`) |
| Data | 22/11/2026 |
| Ferramenta | Claude Code (extensão do VS Code), modelo Claude Opus 5.5 (`claude-opus-5-5`) / SonarQube local no Docker do Ubuntu (WSL 2) / Terminal (`uv run pytest`, `uv run radon`, `uv run mutmut`) |
| Atividade | Corrigir os apontamentos do Sonar da classe `TarifaBancaria` e da tela de tarifas, corrigir o defeito funcional #77 e registrar o print depois (issue #50) |
| Artefatos | `app/dominio/tarifas.py`, `app/templates/tarifas.html`, `tests/unit/test_tarifas.py` |

## Contexto

A inspeção da A2 apontou 7 problemas na funcionalidade de tarifas: 1 em `app/dominio/tarifas.py` (`python:S3776`, complexidade cognitiva 16 em `tarifa_mensal`, limite 15) e 6 de acessibilidade em `app/templates/tarifas.html` (rótulos sem `for` e campos sem `id`). A issue #50 pede corrigir os apontamentos e os bugs funcionais da classe, manter CC ≥ 10, rodar toda a suíte e a mutação e registrar o print depois. O SonarQube do projeto roda em Docker, que foi instalado no Ubuntu (WSL 2) durante a sessão.

## Prompt utilizado

Prompts do responsável, na ordem (transcrição literal):

> 1. "faça a sessão do sonar agora"
> 2. (aprovando o plano apresentado pela IA) "limite 15) em tarifa_mensal tarifas.py:27 Tirar o trecho "com pacote" para um método auxiliar. A melhor forma é reaproveitar o _tarifa_com_pacote, que hoje é código morto, com a regra real. Isso resolve o apontamento e elimina a duplicação. A complexidade ciclomática da classe continua ≥ 10, porque a complexidade só muda de método / 6 apontamentos de acessibilidade (rótulos sem for e campos sem id) tarifas.html Mesma correção que o Pedro fez em credito.html / Defeito funcional #77 (tarifa_anual ignora antiguidade) tarifas.py Corrigir e tirar o xfail. A issue #50 pede para corrigir os bugs funcionais da classe faça isos"
> 3. "preciso instalar o sonar e o docker"
> 4. "preciso que tenha a cc >= 10"

**Resposta da IA:** levantou os 7 apontamentos da A2 e propôs o plano aprovado no prompt 2; a #78 ficou de fora por depender da confirmação do grupo. Gerou a primeira solução: delegação do ramo com pacote para `_tarifa_com_pacote`, `label for`/`id` no HTML e `antiguidade_meses` em `tarifa_anual` (#77). No prompt 3, instalou o Docker no Ubuntu e subiu o SonarQube do `docker-compose.yml` (o SonarQube não precisa de instalação própria: roda como imagem Docker). Ao revisar, a IA avisou que a delegação deixava `tarifa_mensal` com CC 7 e nenhum método da classe com CC ≥ 10. Com o prompt 4, reescreveu a regra do pacote dentro de `tarifa_mensal` como retornos antecipados sem aninhamento (CC 14), removeu `_tarifa_com_pacote` e confirmou com o próprio SonarQube que o apontamento sumiu.

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações. A solução inicial foi gravada no commit `a40d97e` **antes de qualquer revisão**; a revisão está no commit `0322a7d`; a versão final, com o ajuste pedido no prompt 4, está no commit `359f74b`. O diff entre a inicial e a final está em [`sessao-22-diff-sonar-inicial-final.diff`](sessao-22-diff-sonar-inicial-final.diff).

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| **Commit `a40d97e`:** `tarifa_mensal` delegava o ramo com pacote a `_tarifa_com_pacote`, reescrito com a regra real; HTML com `label for`/`id`; `tarifa_anual` com `antiguidade_meses` e `xfail` do #77 removido. **1 failed**, 125 passed, 3 xfailed: o teste da Entrega 1 `corrente_pacote_base` verificava a regra antiga do método morto (30,00). `radon`: `tarifa_mensal` 7, `_tarifa_com_pacote` 6, classe 21 | **Commits `0322a7d` e `359f74b`:** `tarifa_mensal` plana, com retornos antecipados e condições compostas: **CC 14**, complexidade cognitiva ≤ 15; `_tarifa_com_pacote` removido; HTML e #77 como na inicial. **128 passed, 3 xfailed**, 100% de arestas; **Sonar: 0 apontamentos em tarifas**; mutação 92,1% | Revisão da IA (`0322a7d`): teste `corrente_pacote_base` passou a esperar a regra real (15,00); comentários de "código morto" atualizados; #77 virou teste de regressão com o limite 35/36 meses na anual. Ajuste pedido pelo responsável (`359f74b`): regra do pacote volta para `tarifa_mensal` sem aninhamento (CC 12 → 14); `_tarifa_com_pacote` removido e seus testes redirecionados para `tarifa_mensal` com pacote (mesmos valores); `docs/aplicacao.md` atualizado; caso `custom_pacote_meia_tarifa_com_centavos`, motivado pela mutação |

**Como os problemas foram encontrados:** a falha da solução inicial apareceu na execução do pytest. A queda da CC por método foi achada pela IA conferindo `radon cc` contra `docs/aplicacao.md` ("CC ≥ 10 em pelo menos um método"), e o responsável decidiu manter esse requisito (prompt 4). A versão plana foi validada **antes do commit** com uma análise do SonarQube sobre a cópia de trabalho: nenhum apontamento em tarifas. A nova execução do mutmut mostrou 3 sobreviventes novos na linha da meia tarifa (que passou a ser separada): 2 foram mortos pelo caso com corrente 31 (15,50) e 1, que só se distingue em meio centavo, foi justificado.

**Decisão:** a solução final substituiu a delegação pela versão plana, para atender ao requisito de CC ≥ 10 num método sem conflitar com o Sonar. A remoção de `_tarifa_com_pacote` eliminou a regra duplicada e divergente (o método dava 30,00 onde a tela cobrava 15,00); nenhum cenário de teste foi perdido, porque os testes do método passaram a verificar a mesma regra por `tarifa_mensal`. O defeito #78 não foi corrigido: aguarda a confirmação do grupo.

**Validação inicial:** `uv run pytest tests/unit/test_tarifas.py -rfxX` → `1 failed, 125 passed, 3 xfailed` (`test_tarifa_com_pacote[corrente_pacote_base]`), em [`pytest-solucao-inicial.txt`](../../relatorios/evidencias/sonar/depois/tarifas/pytest-solucao-inicial.txt). Análise "antes" no SonarQube (`main`, commit `68d4f53`): 37 apontamentos, 7 de tarifas, em [`antes-main/issues-abertas.json`](../../relatorios/evidencias/sonar/depois/tarifas/antes-main/issues-abertas.json).

**Validação final:** `uv run pytest tests/unit/test_tarifas.py --cov=app.dominio.tarifas --cov-branch` → `128 passed, 3 xfailed`, 100%; `uv run pytest tests/unit tests/integration tests/rnf` → `542 passed` (2 falhas de PIX, #16 e #17, anteriores); `uv run pytest tests/system` → `31 passed`; `uv run radon cc app/dominio/tarifas.py -s` → `tarifa_mensal - C (14)`, em [`pytest-solucao-final.txt`](../../relatorios/evidencias/sonar/depois/tarifas/pytest-solucao-final.txt). SonarQube "depois" (commit `359f74b`): **30 apontamentos, 0 em tarifas**; os 7 com status `CLOSED`/`FIXED`, em [`depois-branch/issues-resolvidas.json`](../../relatorios/evidencias/sonar/depois/tarifas/depois-branch/issues-resolvidas.json) e nos prints [`issues-tarifas-resolvidos.png`](../../relatorios/evidencias/sonar/depois/tarifas/issues-tarifas-resolvidos.png), [`issues-tarifas-abertos.png`](../../relatorios/evidencias/sonar/depois/tarifas/issues-tarifas-abertos.png) e [`dashboard-depois.png`](../../relatorios/evidencias/sonar/depois/tarifas/dashboard-depois.png). Mutação: `101/101 🎉 93 🙁 8` (92,1%), em [`tarifas-execucao-4-pos-sonar.txt`](../../relatorios/evidencias/mutacao/tarifas-execucao-4-pos-sonar.txt).

## Ações executadas

1. Levantados os 7 apontamentos de tarifas no relatório da A2 e apresentado o plano (aprovado no prompt 2).
2. Criada a branch `fix/issue-50-sonar-tarifas`; gerada a solução inicial e gravada sem revisão (`a40d97e`).
3. Revisão: teste da Entrega 1 ajustado à regra real, comentários atualizados, regressão da #77 com o limite 35/36 (`0322a7d`).
4. Instalados o Docker e o Docker Compose no Ubuntu (WSL 2); SonarQube `26.11.0.134175-community` iniciado pelo `docker-compose.yml`; projeto criado e associado ao perfil Sonar way comprehensive (407 regras).
5. Análise "antes" da `main`: 37 apontamentos, 7 de tarifas.
6. Ajuste pedido pelo responsável (CC ≥ 10 num método): `tarifa_mensal` plana com CC 14; `_tarifa_com_pacote` removido; testes redirecionados; análise da cópia de trabalho no SonarQube confirmando 0 apontamentos em tarifas; nova mutação e caso para a meia tarifa; commit `359f74b`.
7. Análise "depois" do commit `359f74b`: 30 apontamentos, 0 em tarifas, 7 `FIXED`; prints do dashboard e das listas de issues (com um usuário local só de leitura, porque a interface exige trocar a senha padrão do `admin`).
8. Atualizados `docs/relatorios/inspecao_sonar.md` (seção 6.2), `docs/relatorios/cobertura_mutacao.md`, `docs/plano_de_teste.md` (v1.16), `docs/aplicacao.md` e o AI-LOG.

## Resultado

- Apontamentos do Sonar na funcionalidade de tarifas: **7 → 0** (`tarifas.py`: 1 → 0; `tarifas.html`: 6 → 0). Projeto: **37 → 30**; Reliability 30 → 24; Maintainability 6 → 5.
- `tarifa_mensal`: complexidade cognitiva 16 → ≤ 15 e **CC 12 → 14**; classe com CC 22.
- Defeito **#77 corrigido** (`tarifa_anual` com 36 meses: 288,00); #78 aguarda o grupo.
- `tests/unit/test_tarifas.py`: **128 passando, 3 `xfail`**, 100% de arestas; mutação **92,1%** (93 de 101).
