# Sessão 26 — Correção do defeito #78 (meia tarifa do pacote premium)

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielcamposs`) |
| Data | 22/11/2026 |
| Ferramenta | Claude Code (extensão do VS Code), modelo Claude Opus 5.5 (`claude-opus-5-5`) / mutmut 3.8 e SonarQube 26.11 no Ubuntu (WSL 2) / Terminal (`uv run pytest`, `radon`, `ruff`) |
| Atividade | Issue #78: corrigir a meia tarifa do pacote da conta premium (15,00 → 25,00), transformar os `xfail` em testes de regressão, validar CC, complexidade cognitiva, cobertura e mutação |
| Artefatos | `app/dominio/tarifas.py`, `tests/unit/test_tarifas.py`, `tests/system/tarifas/test_tarifas_sistema.py`, `docs/relatorios/evidencias/mutacao/tarifas-execucao-5-pos-78.txt`, `docs/relatorios/evidencias/sonar/depois/tarifas-78/` |

## Contexto

O defeito #78 foi revelado na #40 (tabela de decisão, regra R3) e confirmado na interface na #58. Com pacote e saldo ≥ R$ 5.000 ou antiguidade ≥ 24 meses, o cliente paga a "meia tarifa", mas o código calculava metade da tarifa da **corrente** (30 × 0,5 = 15,00) também para a **premium**. A especificação não dizia de qual conta era a metade, por isso o defeito estava "a confirmar pelo grupo", com 4 testes `xfail(strict=True)`: 3 unitários e 1 de sistema.

Antes do prompt técnico abaixo, o responsável pediu à IA que explicasse o defeito ("o que eu preciso para a issue 78, é só corrigir?", "nao entendi ainda o problema"). A IA explicou com uma tabela da premium com pacote por saldo: R$ 4.999,99 → 35,00; R$ 5.000 → 15,00; R$ 50.000 → 0,00. Com a decisão de corrigir para 25,00, a IA fez uma primeira tentativa ("pode corrigir para 25,00", "sim rode novamente o mumut faça doc e feche"). O responsável interrompeu essa tentativa e enviou o prompt técnico abaixo. A pedido dele, a branch voltou para a `main` ("sim, recomece da main e siga o plano"), e os dois commits locais da primeira tentativa, que nunca foram enviados, foram descartados. Esta sessão registra a execução feita a partir do prompt técnico.

## Prompt utilizado

> 1. Prompt técnico (texto integral):
>
> Implemente a issue #78: a meia tarifa do pacote premium usa a tarifa da conta corrente.
> Branch: fix/issue-78-meia-tarifa-premium, a partir da main atualizada. Estou no Windows (PowerShell): use ; em vez de &&.
>
> Decisão do grupo: é defeito no código. A meia tarifa do pacote (saldo >= 5000 ou antiguidade >= 24) deve ser
> 50% da tarifa do próprio tipo de conta, como já acontece no desconto de 30% (premium * 0.7). Premium com
> pacote e saldo 6000 deve dar 25,00 (50 × 0,5); hoje dá 15,00.
>
> Contexto:
> - Em app/dominio/tarifas.py, tarifa_mensal aplica `round(self._base.corrente * 0.5, 2)` na meia tarifa para
>   qualquer tipo de conta.
> - Testes que documentam o defeito, com xfail(strict=True):
>   - tests/unit/test_tarifas.py: test_defeito_pacote_premium_meia_tarifa_da_premium (3 casos);
>   - tests/system/tarifas/test_tarifas_sistema.py: test_defeito_78_pacote_premium_meia_tarifa.
>
> Antes de codar: leia tarifas.py, os dois arquivos de teste e as seções de TarifaBancaria em
> docs/relatorios/cobertura_mutacao.md e docs/relatorios/inspecao_sonar.md (6.4). Rode
> `uv run pytest tests/unit/test_tarifas.py tests/system/tarifas -q` como linha de base e me mostre um plano curto.
> Espere minha aprovação.
>
> O que fazer:
> 1. Corrigir só a linha da meia tarifa, para usar a tarifa do tipo (corrente ou premium) × 0,5. Não mude outras regras.
> 2. Remover o xfail dos 4 testes da #78; eles passam a ser testes de regressão. Ajuste os comentários que dizem
>    "o código devolve 15,00" e o docstring do teste de sistema.
> 3. Acrescentar um caso de regressão que confirme que a corrente continua com 15,00 (corrente + pacote + saldo 6000).
> 4. Restrições:
>    - `uv run radon cc app/dominio/tarifas.py -s`: CC de tarifa_mensal ≥ 10 (hoje é 14) e CC da classe ≥ 10;
>    - a complexidade cognitiva de tarifa_mensal não pode passar de 15 (regra python:S3776 do Sonar, corrigida na #50).
>      Se o SonarQube local estiver disponível (scripts/sonar_local.sh), confirme que tarifas continua com 0 apontamentos;
>      senão, me avise e explique a sua estimativa.
>
> Validação:
> - `uv run pytest tests/unit/test_tarifas.py --cov=app.dominio.tarifas --cov-branch --cov-report=term-missing`: 100% de arestas, sem xfail;
> - `uv run pytest`: suíte inteira verde (só restam os xfail que não são da #78);
> - `uv run pytest tests/system/tarifas -v` e `$env:EVIDENCIAS = "1"; uv run pytest tests/system/tarifas -k 78; Remove-Item Env:EVIDENCIAS`,
>   para gerar o print do caso corrigido (25,00);
> - mutmut só em tarifas.py (receita de classe isolada do README, sem versionar a configuração temporária):
>   escore ≥ 80%; compare com a execução anterior (92,1%, tarifas-execucao-4-pos-sonar.txt) e salve a nova
>   saída em docs/relatorios/evidencias/mutacao/tarifas-execucao-5-pos-78.txt.
>
> Rastreabilidade: um commit com a solução inicial e outro com a revisada. No fim, um resumo com o que mudou,
> a CC antes e depois, o resultado dos comandos e o novo escore de mutação.
>
> Depois da minha aprovação, documentar:
> - docs/aplicacao.md 4.3: escrever a regra da meia tarifa (50% da tarifa do próprio tipo de conta);
> - docs/relatorios/cobertura_mutacao.md e docs/plano_de_teste.md (6.8): #78 corrigido, com a decisão do grupo;
> - docs/relatorios/iso25010.md, se já estiver na main: tirar o #78 dos problemas abertos;
> - AI-LOG: próxima sessão livre, com este prompt.
> Não faça push.
>
> 2. "sim, pode implementar" (aprovação do plano)
> 3. "sim, pode documentar" (aprovação da solução e das evidências)

**Resposta da IA:** a IA rodou a linha de base (`146 passed, 4 xfailed`) e apresentou o plano. Estimou que a CC de `tarifa_mensal` iria de 14 para 15 e que a complexidade cognitiva iria de 12 para 13, dentro do limite. Depois da aprovação, aplicou a correção e os testes. Validou com cobertura, a suíte completa, o Selenium, o print, o mutmut no WSL e duas análises do SonarQube (`main` e branch) num projeto separado. Na entrega, corrigiu a própria estimativa: a complexidade cognitiva subiu **+2**, e não +1, porque a expressão condicional nova fica dentro de um `if` (+1 da expressão e +1 do aninhamento). Também apontou que `tarifa_mensal` deve ter ficado no limite de 15, ainda sem apontamento.

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações. A solução inicial foi gravada no commit `99a05ba` **antes de qualquer revisão**, e a revisada no commit `04a220c`.

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| **Commit `99a05ba`:** em `tarifa_mensal`, `round(self._base.corrente * 0.5, 2)` virou `round((self._base.corrente if tipo is TipoConta.CORRENTE else self._base.premium) * 0.5, 2)`, com um comentário citando a #78; `xfail` removido dos 3 casos `td_r3_premium_*` e de `test_defeito_78_*`, com os comentários e o docstring ajustados; novo caso `td_r3_corrente_pacote_saldo_6000` (corrente + pacote + saldo 6000 → 15,00) | **Commit `04a220c`:** código e testes iguais aos da inicial; acrescentados o print do caso corrigido (R$ 25.00), a saída da nova mutação e as análises do SonarQube | Nenhuma no código nem nos testes. A revisão confirmou: valores esperados sem mudança (já eram 25,00); nenhum outro teste esperava 15,00 para a premium; os 3 mutantes novos foram mortos; Sonar sem apontamento em tarifas |

**Decisão:** a solução da IA foi aceita sem alterações. A regra segue a decisão do grupo informada no prompt: 50% da tarifa do próprio tipo de conta. A sugestão de extrair um método `_tarifa_do_tipo(tipo)` para dar folga na complexidade cognitiva **não foi aplicada**, porque o prompt pede para alterar só a linha da meia tarifa. Os 8 sobreviventes da nova mutação não receberam testes novos, porque são os mesmos padrões já justificados na #45 e na #50.

**Validação inicial** (solução `99a05ba`):
- `uv run ruff check` → ok;
- `uv run radon cc app/dominio/tarifas.py -s` → `tarifa_mensal` C (**14 → 15**); soma dos métodos da classe 23 → 24;
- `uv run pytest tests/unit/test_tarifas.py --cov=app.dominio.tarifas --cov-branch --cov-report=term-missing` → `132 passed`, **100%** (47 statements, 20 ramos), sem `xfail`;
- `uv run pytest` → **`710 passed`**. Não restou nenhum `xfail`, porque os 4 eram da #78;
- `uv run pytest tests/system/tarifas -v` → `19 passed`;
- `$env:EVIDENCIAS = "1"; uv run pytest tests/system/tarifas -k 78` → print com **R$ 25.00**.

**Validação final:**
- **mutmut** só em `tarifas.py`, numa cópia no WSL com `only_mutate` (não versionado): **104 mutantes, 96 mortos (92,3%)**, contra 101 / 93 (92,1%) na execução 4. Os 8 sobreviventes são os mesmos padrões, comparados um a um ([`tarifas-execucao-5-pos-78.txt`](../../relatorios/evidencias/mutacao/tarifas-execucao-5-pos-78.txt)).
- **SonarQube**, no projeto separado `banco-digital-uff-2026-2-issue78`, com o perfil comprehensive: `main` e branch com 19 apontamentos no projeto e **0 em `tarifas.py`**, sem `python:S3776`. A complexidade cognitiva do arquivo foi de 17 para 19 ([`resumo.txt`](../../relatorios/evidencias/sonar/depois/tarifas-78/resumo.txt)).
- Revisão e aprovação do responsável (prompt 3).

## Ações executadas

1. A branch `fix/issue-78-meia-tarifa-premium` voltou para a `main` (`8d8dbb5`), descartando a primeira tentativa (local, sem push).
2. Leitura de `tarifas.py`, dos testes e das seções de `TarifaBancaria` nos relatórios; linha de base `146 passed, 4 xfailed`; plano aprovado (prompt 2).
3. Correção de uma linha, remoção dos 4 `xfail`, caso novo da corrente; solução inicial gravada sem revisão (`99a05ba`).
4. Validação: cobertura, suíte completa, Selenium, print, mutmut no WSL e SonarQube (`main` e branch); versão revisada com as evidências (`04a220c`).
5. Documentação (prompt 3):
   - `docs/aplicacao.md`: regra da meia tarifa e CC 15;
   - `docs/relatorios/cobertura_mutacao.md`: tabela R3, defeitos e nota da #78;
   - `docs/plano_de_teste.md` (v1.25): estado atual, 6.2 e 6.8, com a decisão do grupo;
   - `docs/relatorios/iso25010.md`: #78 fora dos problemas abertos, adequação funcional 4 → 5;
   - `AGENTS.md` e o AI-LOG.

## Resultado

- **Defeito #78 corrigido:** a premium com pacote e saldo ≥ 5.000 (ou 24 meses) paga **R$ 25,00**; antes pagava 15,00. A corrente continua com 15,00.
- `uv run pytest` → **710 passed**, sem `xfail`. Cobertura de arestas de `tarifas.py` em 100%.
- CC de `tarifa_mensal` 14 → **15**; SonarQube: 0 apontamentos em tarifas.
- Mutação de `TarifaBancaria`: **92,3%** (99,0% descontando os 7 equivalentes).
