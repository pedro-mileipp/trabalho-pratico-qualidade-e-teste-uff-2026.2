# Sessão 21 — Teste de mutação de `TarifaBancaria` (issue #45)

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielcamposs`) |
| Data | 22/11/2026 |
| Ferramenta | Claude Code (extensão do VS Code), modelo Claude Opus 5.5 (`claude-opus-5-5`) / Terminal Ubuntu no WSL 2 (`uv run mutmut`) |
| Atividade | Aplicar a técnica baseada em defeitos (mutação) em `TarifaBancaria` e atingir escore ≥ 80% (issue #45) |
| Artefatos | `tests/unit/test_tarifas.py` |

## Contexto

Aplicar o teste de mutação com `mutmut` à classe `TarifaBancaria` (`app/dominio/tarifas.py`), usando a suíte de `tests/unit/test_tarifas.py` ampliada na #40 (122 casos, 100% de cobertura de arestas), e atingir escore ≥ 80%. O mutmut 3 não roda nativamente no Windows, então foram instalados o WSL 2 e o Ubuntu, e o projeto é copiado para o Linux só para executar a mutação. O código e os commits continuam no repositório do Windows.

Antes do prompt, o responsável pediu orientação ("ta quero fazer o teste de mutação agora explique o que preciso fazer") e **executou ele mesmo a primeira rodada do mutmut** no terminal do Ubuntu: 106 mutantes, 87 mortos e 19 sobreviventes (82,1%). A IA gravou a evidência com o diff de cada sobrevivente e propôs uma triagem. Em seguida, o responsável enviou o prompt abaixo.

## Prompt utilizado

> "O mutmut sobre app/dominio/tarifas.py gerou 106 mutantes: 87 mortos e 19 sobreviventes (82,1%). Analise os sobreviventes em docs/relatorios/evidencias/mutacao/tarifas-execucao-1-antes.txt, justifique os equivalentes e crie testes em tests/unit/test_tarifas.py que matem os demais, identificando a técnica no id (custom_, vl_), sem alterar app/dominio/tarifas.py"

**Resposta da IA:** classificou os 19 sobreviventes em 6 equivalentes e 13 matáveis. Os 6 equivalentes são: padrões de parâmetro 0 → 1 (3 mutantes), `<=` → `<` no limite da cota e dois `round(..., 2)` → `round(..., 3)` desfeitos por arredondamentos seguintes. Para estes dois últimos, a IA verificou por varredura que nenhum valor de R$ 0,01 a R$ 20.000,00 distingue o mutante. Os 13 matáveis tinham uma causa comum: as tarifas padrão (30, 50 e 2,50) são valores redondos, então nenhum teste dependia dos `round`. A IA criou 7 casos: 5 com `TarifasBase` em centavos (`custom_`), 1 de limite (`vl_`, premium com saldo exatamente 50000) e 1 com valores padrão (`pe_`, `tarifa_anual` sem informar o pacote).

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações quando a IA é usada na geração de testes. A solução inicial foi gravada no commit `145bd2d` **antes de qualquer revisão**; a final está no commit `21e9824`; o diff entre as duas está em [`sessao-21-diff-mutacao-inicial-final.diff`](sessao-21-diff-mutacao-inicial-final.diff).

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| 7 casos novos (129 no total, **125 passando e 4 `xfail`**). Mutação: **100 mortos, 6 sobreviventes, 94,3%**. Os 6 sobreviventes eram exatamente os classificados como equivalentes. Os comentários identificavam cada mutante só pelo número (`mutmut_26`...), não avisavam que os testes de `_tarifa_com_pacote` cobrem código morto e não explicavam a escolha dos valores com centavos | Mesmos 7 casos e mesmos valores esperados (**125 passando e 4 `xfail`**). Mutação: **100 mortos, 6 sobreviventes equivalentes, 94,3%** (100% descontando os equivalentes) | Comentários passaram a descrever a mutação em texto (ex.: `round(base * 0.8, 2) -> round(..., None)`), porque os números dos mutantes mudam quando `tarifas.py` muda (ex.: na correção de #77/#78); aviso de que os testes de `_tarifa_com_pacote` devem sair junto se a #50 remover o método; justificativa dos valores (evitar meio centavo exato, em que o arredondamento de `float` é ambíguo) |

**Decisão:** os casos e os valores esperados gerados pela IA foram aceitos sem alteração, depois de conferidos à mão (ex.: 50,01 × 0,7 = 35,007 → 35,01; 30,01 + 30,01 × 0,2 = 36,012 → 36,01; 31 × 0,8 = 24,80). A revisão alterou só os comentários, pelos três motivos acima. Os 6 sobreviventes restantes foram aceitos como equivalentes, com justificativa em `docs/relatorios/cobertura_mutacao.md`. O código de domínio em `app/dominio/tarifas.py` foi mantido sem alterações.

**Validação inicial:** execução 1, pelo responsável, no Ubuntu: `uv run mutmut run --max-children 4` → `106/106 🎉 87 🙁 19` (82,1%), em [`tarifas-execucao-1-antes.txt`](../../relatorios/evidencias/mutacao/tarifas-execucao-1-antes.txt). Execução 2, com a solução inicial da IA → `106/106 🎉 100 🙁 6` (94,3%), em [`tarifas-execucao-2-solucao-inicial.txt`](../../relatorios/evidencias/mutacao/tarifas-execucao-2-solucao-inicial.txt).

**Validação final:** `uv run pytest tests/unit/test_tarifas.py` → `125 passed, 4 xfailed`; `uv run ruff check tests/unit/test_tarifas.py` → `All checks passed!`. Execução 3 (`uv run mutmut run --max-children 4`) → `106/106 🎉 100 🙁 6` (**94,3%**; 100 / 100 descontando os equivalentes), em [`tarifas-execucao-3-final.txt`](../../relatorios/evidencias/mutacao/tarifas-execucao-3-final.txt). Mapeamento: cada um dos 13 mutantes foi aplicado sozinho (`mutmut apply`), rodando só os testes novos, e todos foram mortos exatamente pelo caso indicado no comentário, em [`tarifas-mapeamento-mutante-teste.txt`](../../relatorios/evidencias/mutacao/tarifas-mapeamento-mutante-teste.txt). Equivalentes `tarifa_mensal__mutmut_49` e `tarifa_anual__mutmut_17`: varredura de R$ 0,01 a R$ 20.000,00 sem nenhum valor que distinga o mutante.

## Ações executadas

1. Instalados o WSL 2 e o Ubuntu; instalado o `uv` no Ubuntu; o projeto passou a ser copiado para `~/projeto`, com a restrição `only_mutate`/`pytest_add_cli_args_test_selection` aplicada só na cópia.
2. Criada a branch `test/issue-45-mutacao-tarifas` a partir da branch da #40 (suíte de 122 casos).
3. Execução 1 do mutmut pelo responsável (82,1%); a IA gravou a evidência com o diff dos 19 sobreviventes.
4. Triagem: 6 equivalentes, 2 deles comprovados por varredura de valores; 13 matáveis.
5. Gerados os 7 casos novos; solução gravada sem revisão (`145bd2d`) e execução 2 do mutmut (94,3%).
6. Revisão: conferido o mapeamento mutante → teste (13/13); comentários corrigidos; solução final gravada (`21e9824`) e execução 3 do mutmut (94,3%).
7. Atualizados `docs/relatorios/cobertura_mutacao.md` (subseção "Mutação — #45" e nota no piloto da #36), `docs/plano_de_teste.md` (v1.15, seção 6.8) e o AI-LOG.

## Resultado

- **129 casos** em `tests/unit/test_tarifas.py` (+7): **125 aprovados e 4 `xfail`** (defeitos #77 e #78).
- Escore de mutação de `TarifaBancaria`: **69,8% (piloto) → 82,1% (após a #40) → 94,3%** (106 mutantes, 100 mortos); **100%** descontando os 6 equivalentes justificados.
- Causa dos sobreviventes identificada: as tarifas padrão redondas não exercitavam os arredondamentos; os casos `custom_` com centavos passaram a exercitá-los.
- 4 dos mutantes mortos estão em `_tarifa_com_pacote` (código morto); se a #50 remover o método, os testes saem junto e o escore deve ser recalculado.
