# Sessão 14 — Testes unitários com mock de `TransacaoService` (issue #53)

| Campo | Valor |
|---|---|
| Responsável | Gabrielle Rosa (`n2Gabrielle`) |
| Data | 20/11/2026 |
| Ferramenta | Gemini / VS Code / Terminal (`.venv/bin/pytest`) |
| Atividade | Projetar, validar e executar testes unitários isolados de `TransacaoService` com mock de `Repositorio` e `TransacaoPix` (issue #53) |
| Artefatos | `tests/unit/test_transacao_service.py` |

## Contexto

Implementar testes unitários da classe `TransacaoService` (`app/servicos/transacoes.py`) isolando `Repositorio` via `pytest-mock` (`mocker.Mock(spec=Repositorio)`), sem acesso a SQLite ou Flask, cobrindo cliente inexistente, PIX recusado sem escrita no repositório e PIX aprovado com verificação de argumentos e mock de `TransacaoPix`.

## Prompt utilizado

> "Com base no código abaixo de TransacaoService, TransacaoPix e Repositorio, gere testes unitários em Python usando pytest e pytest-mock (mocker.Mock(spec=Repositorio)) para o arquivo tests/unit/test_transacao_service.py, sem acessar SQLite ou Flask. Cubra obrigatoriamente: cliente inexistente, PIX recusado sem chamar atualizar_saldo/registrar_transacao, PIX aprovado com novo saldo e argumentos corretos; opcionalmente mockar também o TransacaoPix."

**Resposta da IA:** gerou `tests/unit/test_transacao_service.py` com 4 testes em `TestTransferirPix`, verificando `assert_not_called()` em recusas e `assert_called_once_with(...)` na aprovação.

## Solução inicial (gerada pela IA) vs. solução final (após validação)

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| 4 testes com patch em `app.servicos.transacao_service.TransacaoPix`, chave `"+5511999999999"` (`ChaveTipo.TELEFONE`) e `horario` como `datetime` | 4 testes com patch em `app.servicos.transacoes.TransacaoPix`, chave válida `"maria@exemplo.com"` (`ChaveTipo.EMAIL`) e `horario` como `datetime.time`, todos aprovados | Corrigidos o caminho do `mocker.patch` para `app.servicos.transacoes.TransacaoPix`, o tipo/chave PIX para `ChaveTipo.EMAIL` (evitando `TransacaoRecusada: chave_invalida`) e o tipo de `horario` para `time(...)` (evitando `TypeError` entre `datetime` e `time` em `TransacaoPix._eh_noturno`) |

**Decisão:** todas as correções foram validadas manualmente e aplicadas em `tests/unit/test_transacao_service.py`; o código de produção não foi alterado.

**Validação inicial:** `.venv/bin/pytest tests/unit/test_transacao_service.py -v` → `2 failed, 2 passed` (falha de módulo inexistente e `chave_invalida`), depois `1 failed, 3 passed` (`TypeError` com `datetime` em `_eh_noturno`).

**Validação final:** `.venv/bin/pytest tests/unit/test_transacao_service.py -v` → `4 passed in 0.12s`[cite: 7].

## Ações executadas

1. Revisado `app/servicos/transacoes.py`, `app/dominio/pix.py` e `Repositorio`.
2. Criado `tests/unit/test_transacao_service.py` com `mocker.Mock(spec=Repositorio)` e teste com `TransacaoPix` mockado.
3. Ajustado o patch para `app.servicos.transacoes.TransacaoPix`, a chave/tipo para `ChaveTipo.EMAIL` e `horario` para `time(...)`.
4. Executada e validada a suíte com `.venv/bin/pytest tests/unit/test_transacao_service.py -v` (`4 passed in 0.12s`)[cite: 7].

## Resultado

- **4 testes aprovados** em `tests/unit/test_transacao_service.py` sem acesso a SQLite ou Flask[cite: 7].
- Verificado que cliente inexistente e PIX recusado não chamam `atualizar_saldo` nem `registrar_transacao`, e que PIX aprovado retorna o novo saldo e chama os mocks com os argumentos esperados.