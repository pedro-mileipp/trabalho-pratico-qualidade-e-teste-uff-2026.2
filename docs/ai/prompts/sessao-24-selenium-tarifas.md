# Sessão 24 — Testes de sistema Selenium de Tarifas (issue #58)

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielcamposs`) |
| Data | 22/11/2026 |
| Ferramenta | Claude Code (extensão do VS Code), modelo Claude Opus 5.5 (`claude-opus-5-5`) / Selenium WebDriver 4 com Chrome headless / Terminal (`uv run pytest`, `ruff`) |
| Atividade | Issue #58: testes de sistema com Selenium do fluxo de Tarifas (RF04), automatizando os casos manuais CT-01 a CT-15 |
| Artefatos | `tests/system/tarifas/pagina_tarifas.py`, `tests/system/tarifas/test_tarifas_sistema.py`, `tests/system/tarifas/evidencias/`, `app/templates/tarifas.html` (só os atributos `id="pacote"` e `id="tarifa-resultado"`) |

## Contexto

As telas de crédito (#60), autenticação (#57) e empréstimo (#59) já tinham testes de sistema, com a base compartilhada em `tests/system/conftest.py`. A #58 cobre a tela de tarifas, com os casos do caso manual da Entrega 1 (`tests/testes_manuais/tarifas/caso_tarifas.md`). Linha de base antes da sessão: `uv run pytest tests/system -q` → **31 passed**.

## Prompt utilizado

> 1. Prompt técnico (texto integral):
>
> Implemente a issue #58: testes de sistema com Selenium do fluxo de Tarifas (RF04).
>
> Contexto:
> - Reutilize tests/system/conftest.py (servidor Flask em thread, Chrome headless, cliente_logado, evidencia,
>   screenshot + HTML em falhas/). Não altere o conftest.
> - Motivo: o conftest já atende aos critérios da issue (banco isolado, testes independentes, evidência de falha)
>   e é usado pelos testes de auth, crédito e empréstimo; alterá-lo poderia quebrá-los. Se precisar de algo
>   específico de Tarifas, coloque no page object ou num tests/system/tarifas/conftest.py.
> - Siga o padrão de tests/system/credito/ (page object + testes parametrizados).
> - Referência: tests/testes_manuais/tarifas/caso_tarifas.md (CT-01 a CT-15).
>
> Antes de codar: leia esses arquivos, rode `uv run pytest tests/system -q` e me mostre um plano curto. Espere minha aprovação.
>
> O que fazer em tests/system/tarifas/:
> 1. pagina_tarifas.py: abrir, preencher(tipo, saldo, transacoes, pacote), enviar e tarifa_exibida() -> float.
> 2. test_tarifas_sistema.py:
>    - CT-01 a CT-15 parametrizados, com os ids do caso manual, comparando o valor exibido;
>    - recusas: saldo e transações negativos barrados pelo formulário, e /tarifas sem login redireciona para /login;
>    - 1 caso da #78 (premium + pacote + saldo 6000 → esperado 25,00) com xfail(strict=True, reason="#78").
>      Antes, confirme o valor que a tela mostra hoje.
> 3. Seletores por ID/NAME, WebDriverWait (sem sleep), testes independentes e determinísticos, sem mocks.
>    Pode acrescentar apenas atributos id no template (checkbox e resultado). Não mude mais nada em app/.
>
> Validação: `uv run pytest tests/system -q` verde; `EVIDENCIAS=1 uv run pytest tests/system/tarifas`;
> quebre um esperado de propósito para provar que falhas/ recebe screenshot e HTML, e depois desfaça.
>
> Rastreabilidade: um commit com a solução inicial e outro com a revisada. No fim, um resumo com os casos,
> os resultados e o que mudou.
>
> Depois da minha aprovação: seção "Tarifas (RF04) — Daniel Izu" na 6.2 do Plano de Teste, linha no README,
> e uma sessão no AI-LOG com este prompt. Não faça push.
>
> 2. Aprovação do plano (texto integral):
>
> Aprovado. Pode implementar.
> - Faça tem_resultado() com find_elements, sem WebDriverWait, para os testes de recusa não esperarem 5 s.
> - Além da suíte completa, rode um caso isolado: uv run pytest tests/system/tarifas -k ct09 -v
> - No AI-LOG, use a próxima sessão livre (a 22 já existe).
> - Estou no Windows (PowerShell): use ; em vez de && e $env:EVIDENCIAS = "1" para as evidências.
>
> 3. "validei aqui e realmente o #78 acontece"
> 4. "sim, faça isso" (aprovação da documentação e do comentário na issue #78)

**Resposta da IA:** a IA leu o `conftest.py` compartilhado, os testes e o page object de crédito, o template e a rota de tarifas e o caso manual. Rodou a linha de base (31 passed) e, antes do plano, postou os 15 casos e o da #78 no `/tarifas` pelo cliente de testes do Flask: os 15 valores bateram com o caso manual, e o caso da #78 mostrou 15,00. Apresentou o plano (2 ids no template, page object e 19 casos) e, depois da aprovação, implementou seguindo os ajustes do prompt 2. Confirmou o valor da #78 também no Chrome, com `--runxfail`.

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações. A solução inicial foi gravada no commit `850f87d` **antes de qualquer revisão**, e a final no commit `afe29fa`; o diff do código está em [`sessao-24-diff-selenium-inicial-final.diff`](sessao-24-diff-selenium-inicial-final.diff).

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| **Commit `850f87d`:** `id="pacote"` e `id="tarifa-resultado"` em `tarifas.html`; `pagina_tarifas.py` (`abrir`, `preencher`, `enviar`, `tarifa_exibida`, `tem_resultado` sem espera, `campo_abaixo_do_minimo`); `test_tarifas_sistema.py` com 19 casos. `tests/system/tarifas`: 18 passed, 1 xfailed. O `ruff` apontava `PYI041` (anotação redundante `float \| str \| int` em `_preencher`) | **Commit `afe29fa`:** igual nos testes; `ruff` ok; 37 prints de evidência acrescentados | Corrigida a anotação para `float \| str`, sem mudança de comportamento, e acrescentadas as evidências geradas com `EVIDENCIAS=1`. Os casos, os seletores e os valores esperados ficaram iguais aos da solução inicial |

**Decisão:** a solução da IA foi aceita com a correção de lint. O caso da #78 ficou com `xfail(strict=True, reason="#78")`, porque a correção depende da decisão do grupo. Quando o defeito for corrigido, o teste passa a dar `XPASS` e falha pelo `strict`, o que obriga a remover a marcação. Não foi criado um `tests/system/tarifas/conftest.py`, porque o page object resolveu o que era específico de tarifas.

**Validação inicial:** `uv run pytest tests/system/tarifas -v` → `18 passed, 1 xfailed`; `--runxfail -k defeito_78` → `assert 15.0 == 25.0` (a tela mostra 15,00 no Chrome); `uv run ruff check tests/system/tarifas` → 1 apontamento (`PYI041`).

**Validação final:** `uv run ruff check tests/system/tarifas` → `All checks passed!`; `uv run pytest tests/system -q` → `49 passed, 1 xfailed`, e os 31 testes anteriores continuam passando; `uv run pytest tests/system/tarifas -k ct09 -v` → `1 passed`; `$env:EVIDENCIAS = "1"; uv run pytest tests/system/tarifas` → `18 passed, 1 xfailed` e 37 prints em `tests/system/tarifas/evidencias/`. **Falha forçada:** o esperado do CT-09 foi trocado de 32,50 para 99,99, e o teste falhou com `assert 32.5 == 99.99`; `tests/system/tarifas/falhas/` recebeu o `.png` (26 KB) e o `.html` (2,5 KB) (pasta fora do git); o esperado foi restaurado e o CT-09 voltou a passar. **Validação humana:** o responsável reproduziu o caso na tela (premium, pacote, saldo 6000 → R$ 15,00 em vez de R$ 25,00) e confirmou o defeito #78 (prompt 3).

## Ações executadas

1. Criada a branch `test/issue-58-selenium-tarifas` a partir da `main` (`ac7bd48`); linha de base: 31 passed.
2. Valores atuais da tela conferidos pelo cliente de testes do Flask (15 casos e o da #78); plano apresentado e aprovado com ajustes (prompt 2).
3. Acrescentados os 2 ids no template; criados o page object e os testes; valor da #78 confirmado no Chrome; solução inicial gravada sem revisão (`850f87d`).
4. Revisão: correção do `PYI041`, suíte completa, caso isolado, evidências e falha forçada; versão revisada gravada (`afe29fa`).
5. Validação manual da #78 pelo responsável (prompt 3).
6. Atualizados `docs/plano_de_teste.md` (v1.19, seção 6.2), o `README.md` e o AI-LOG; comentário na issue #78 registrando que o defeito aparece na interface.

## Resultado

- **19 testes de sistema de tarifas:** CT-01 a CT-15, 2 recusas do formulário e o acesso sem login passando, e 1 `xfail` da #78. Suíte `tests/system`: **31 → 49 passed, 1 xfailed**.
- **Defeito #78 confirmado na interface:** a tela mostra R$ 15,00 em vez de R$ 25,00. A confirmação veio pelo Selenium e pela validação manual do responsável.
- `app/` alterado só nos 2 atributos `id` do template; `conftest.py` compartilhado sem alterações.
