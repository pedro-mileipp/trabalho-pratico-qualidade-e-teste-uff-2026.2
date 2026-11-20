# Sessão 13 — Testes unitários com mock de `AuthService` (issue #53)

| Campo | Valor |
|---|---|
| Responsável | Gabrielle Rosa (`n2Gabrielle`) |
| Data | 20/11/2026 |
| Ferramenta | Gemini / VS Code / Terminal (`.venv/bin/pytest`) |
| Atividade | Projetar, validar e executar testes unitários isolados de `AuthService` com mock de `Repositorio` (issue #53) |
| Artefatos | `tests/unit/test_auth_service.py` |

## Contexto

Implementar testes unitários da classe `AuthService` (`app/servicos/auth.py`) isolando `Repositorio` via `pytest-mock` (`mocker.Mock(spec=Repositorio)`), sem acesso a SQLite ou Flask, cobrindo `registrar` e `autenticar` e verificando chamadas nos mocks.

## Prompt utilizado

> "Com base no código abaixo de AuthService e na interface de Repositorio, gere testes unitários em Python usando pytest e pytest-mock (mocker.Mock(spec=Repositorio)) para o arquivo tests/unit/test_auth_service.py, sem nenhum acesso a SQLite ou Flask. Cubra obrigatoriamente: campos vazios, nome/e-mail com espaços, senha 5 vs. 6 caracteres, e-mail duplicado (EmailJaCadastrado), e-mail em minúsculas, senha salva como hash; autenticar com cliente inexistente, senha errada, e-mail com maiúsculas/espaços e sucesso."

**Resposta da IA:** gerou a estrutura inicial de `tests/unit/test_auth_service.py` com fixtures de `Repositorio` mockado, `AuthService` e casos parametrizados para `TestRegistrar` e `TestAutenticar`.

## Solução inicial (gerada pela IA) vs. solução final (após validação)

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| Suíte com 12 testes gerada para `app.servicos.auth_service` e instanciação de `Cliente` sem `saldo` | Suíte com 12 testes importando `app.servicos.auth` e passando `saldo` em todas as instâncias de `Cliente`, com os 12 testes aprovados | Corrigido o caminho de importação para `app.servicos.auth` e adicionado o argumento obrigatório `saldo` (`0.0`) no `side_effect` de `criar_cliente` e nas instâncias diretas de `Cliente` após falha de coleta e `TypeError` na execução |

**Decisão:** os ajustes de importação e do parâmetro `saldo` foram validados manualmente e mantidos; o código de produção em `app/servicos/auth.py` não precisou ser alterado.

**Validação inicial:** `.venv/bin/pytest tests/unit/test_auth_service.py -v` → `ModuleNotFoundError` (`app.servicos.auth_service`), depois `7 passed, 5 failed` e `9 passed, 3 failed` (`TypeError: Cliente.__init__() missing 1 required positional argument: 'saldo'`).

**Validação final:** `.venv/bin/pytest tests/unit/test_auth_service.py -v` → `12 passed in 2.96s`[cite: 6].

## Ações executadas

1. Revisado `app/servicos/auth.py` e a interface `Repositorio`.
2. Criado `tests/unit/test_auth_service.py` com `mocker.Mock(spec=Repositorio)`.
3. Ajustado o import para `app.servicos.auth` e incluído `saldo` nas instâncias de `Cliente`.
4. Executada e validada a suíte completa com `.venv/bin/pytest tests/unit/test_auth_service.py -v` (`12 passed in 2.96s`)[cite: 6].

## Resultado

- **12 testes aprovados** em `tests/unit/test_auth_service.py` sem acesso a SQLite ou Flask[cite: 6].
- Cobertos campos vazios, normalização de espaços e e-mail em minúsculas, fronteira de senha (5 vs. 6 caracteres), `EmailJaCadastrado`, hash de senha e cenários de `autenticar`.