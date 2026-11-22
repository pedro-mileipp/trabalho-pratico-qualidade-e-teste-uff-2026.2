# Sessão 23 — Testes de integração serviços ↔ repositório (issue #54)

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielcamposs`) |
| Data | 22/11/2026 |
| Ferramenta | Claude Code (extensão do VS Code), modelo Claude Opus 5.5 (`claude-opus-5-5`) / Terminal (`uv run pytest`, `pytest-cov`, `ruff`) |
| Atividade | Issue #54: testes de integração entre `AuthService`/`TransacaoService` e os repositórios reais (`SqliteRepositorio` e `MemoriaRepositorio`), sem mocks |
| Artefatos | `tests/integration/conftest.py` (fixtures novas), `tests/integration/test_servicos_repositorio.py`, `tests/integration/test_contrato_repositorio.py`, `docs/relatorios/evidencias/integracao/servicos-repositorio.txt` |

## Contexto

O enunciado exige testes de integração. A #55 (Vinicius) já testava as rotas HTTP com o `test_client` e tinha criado `tests/integration/conftest.py`. A #54 pede outro nível: os serviços chamados diretamente sobre o repositório real, sem HTTP e sem mocks, e o mesmo contrato verificado também no `MemoriaRepositorio`. Linha de base antes da sessão: `uv run pytest tests/integration -q` → **28 passed**.

## Prompt utilizado

> 1. Prompt técnico (texto integral):
>
> Você vai implementar a issue #54 do repositório: "test: integração serviços ↔ SqliteRepositorio".
> Trabalhe na branch test/issue-54-integracao-servicos-repositorio, criada a partir da main atualizada.
>
> ## Contexto
> - O enunciado da disciplina exige testes de integração. Os testes devem usar as camadas reais, SEM mocks.
> - SqliteRepositorio (app/repositorios/sqlite_repositorio.py) recebe uma factory de conexão; use get_db
>   (app/db.py) dentro de app.app_context(), com DATABASE apontando para um arquivo em tmp_path.
> - tests/integration/conftest.py JÁ EXISTE (criado na issue #55, testes de rotas com test_client), com as
>   fixtures app, cliente, conexao_banco, cliente_autenticado e definir_saldo. NÃO recrie nem altere essas
>   fixtures; apenas acrescente as novas. Os 28 testes de tests/integration/test_rotas.py devem continuar passando.
> - Diferença para a #55: lá o teste passa pelas rotas HTTP; aqui o teste chama AuthService e TransacaoService
>   diretamente sobre o repositório real, sem Flask/HTTP (o app só fornece o contexto e o banco temporário).
>
> ## Antes de escrever código
> 1. Leia app/repositorios/*.py, app/servicos/*.py, app/db.py, app/config.py, app/dominio/pix.py,
>    tests/integration/conftest.py e tests/integration/test_rotas.py.
> 2. Rode `uv run pytest tests/integration -q` e salve o resultado como linha de base.
> 3. Me apresente um plano curto (fixtures + lista de casos) e espere minha aprovação antes de implementar.
>
> ## O que fazer
> 1. Fixtures novas em tests/integration/conftest.py:
>    - repo_sqlite: SqliteRepositorio(get_db) dentro de app.app_context() (use yield);
>    - repo_memoria: MemoriaRepositorio();
>    - repositorio: parametrizada em ["sqlite", "memoria"] via request.getfixturevalue, para rodar o mesmo
>      contrato nas duas implementações.
> 2. tests/integration/test_servicos_repositorio.py (parametrizado nos dois repositórios):
>    - AuthService registra e autentica um cliente real: mesmo id; e-mail salvo em minúsculas e sem espaços;
>      senha_hash começa com "pbkdf2:sha256" e é diferente da senha;
>    - e-mail duplicado → EmailJaCadastrado; senha errada e e-mail inexistente → CredenciaisInvalidas;
>    - TransacaoService: PIX aprovado (saldo 1000, PIX 300) → retorno 700, saldo 700 no repositório e
>      listar_transacoes com 1 item (tipo "pix", valor -300, descricao "PIX email");
>    - dois PIX seguidos: saldo acumulado correto e extrato com 2 itens na ordem;
>    - transferência recusada NÃO altera saldo nem extrato: saldo insuficiente, chave inválida e limite
>      noturno (horario=time(22, 0), valor 1500 → FORA_HORARIO). Verifique o ResultadoPix em
>      TransacaoRecusada.resultado;
>    - cliente inexistente → TransacaoRecusada;
>    - o PIX do cliente A não aparece no extrato do cliente B;
>    - só SQLite: os dados persistem em um app.app_context() novo (conexão nova) e conferem com SELECT
>      direto pela fixture conexao_banco.
> 3. tests/integration/test_contrato_repositorio.py (chamando o Repositorio diretamente, nas duas implementações):
>    - criar_cliente cria com saldo 0 e score 500; buscar por id e por e-mail encontram; inexistentes → None;
>    - atualizar_saldo e atualizar_score persistem; registrar_transacao devolve data em ISO;
>      listar_transacoes mantém a ordem de inserção.
>    - Divergências entre as implementações (NÃO altere o código de produção): e-mail duplicado direto no
>      repositório (SQLite: sqlite3.IntegrityError pelo UNIQUE; memória: aceita) e atualizar_saldo com id
>      inexistente (SQLite: não faz nada; memória: KeyError). Fixe o comportamento atual em testes separados
>      por implementação, com um comentário explicando a divergência. Confirme rodando antes de afirmar.
> 4. Garantir que nenhum banco.db seja criado no workspace: um teste confirma que app.config["DATABASE"]
>    está dentro de tmp_path, e uma fixture autouse no módulo compara a existência/mtime de banco.db na
>    raiz antes e depois (não falhe só porque já existe um banco.db local).
>
> ## Regras
> - SEM mocks (nada de mocker, unittest.mock ou monkeypatch de serviço/repositório).
> - Banco isolado por teste (tmp_path), sem limpeza manual e sem depender da ordem dos testes.
> - Sempre passe horario=time(...) (datetime.time) no transferir_pix. O serviço anota `datetime`, mas o
>   domínio espera `time`, e sem horário o teste depende da hora em que roda (o limite noturno começa às 20h).
>   Registre essa inconsistência de tipo como observação; não corrija o código.
> - Não use chave de e-mail com dois "@" (bug #16, aberto) nem chargeback (bug #17).
> - Não altere nada em app/. Se achar um defeito, pare e me informe.
> - Nomes de testes e comentários em português, no estilo de tests/integration/test_rotas.py.
>
> ## Validação
> - `uv run pytest tests/integration -q` verde (os 28 da #55 + os novos).
> - `uv run pytest tests/integration -v --cov=app.servicos --cov=app.repositorios --cov-branch
>   --cov-report=term-missing --cov-fail-under=0`, salvando a saída em
>   docs/relatorios/evidencias/integracao/servicos-repositorio.txt.
> - `uv run pytest`: só podem falhar os 2 testes do PIX (#16 e #17), que são de outra issue.
>
> ## Rastreabilidade da IA (exigida pelo enunciado)
> - Faça um commit com a solução inicial antes de qualquer ajuste meu, e outro commit com a versão revisada,
>   para preservar a solução inicial e a final.
> - No fim, me entregue um resumo: casos criados por arquivo, resultado dos comandos, cobertura obtida,
>   divergências encontradas e o que foi alterado entre a solução inicial e a final.
>
> ## Documentação (depois de eu aprovar os testes)
> - docs/plano_de_teste.md: nova seção 6.x "Integração serviços ↔ repositório — Daniel Izu (#54)", com
>   escopo (diferença para a #55), tabela de casos, resultado e divergências; acrescente a linha no
>   Registro de Mudanças.
> - README.md: os 2 arquivos novos na tabela de estrutura e o comando na seção "Testes de integração".
> - docs/ai/AI-LOG.md: linha da sessão (Responsável: Daniel Izu; Ferramenta: Claude Code, modelo usado;
>   Prompt; Resultado; Decisão; Validação) e o arquivo docs/ai/prompts/sessao-NN-integracao-servicos-repositorio.md
>   com este prompt e o resumo. Use o próximo número livre de sessão.
> - Não faça push nem abra PR; eu reviso e envio.
>
> 2. "pode implementar e apague a branch vazia eu realizar a validação" (aprovação do plano)
> 3. "aplique o ajuste e para a documentação" (aprovação do ajuste proposto na revisão)

**Resposta da IA:** a IA leu os arquivos pedidos, rodou a linha de base (28 passed, nenhum `banco.db` na raiz) e apresentou o plano: 3 fixtures novas e as classes de teste com a lista de casos. Depois da aprovação (prompt 2), implementou os dois arquivos e as fixtures, confirmou as duas divergências rodando os testes e gravou a solução inicial sem revisão. Na revisão da cobertura, apontou que a linha 27 de `app/servicos/auth.py` (`raise CredenciaisInvalidas("senha muito curta")`) não era exercitada pelos testes de integração. A linha de campos vazios só aparecia coberta por causa de um teste de rota da #55. A IA propôs um caso de registro inválido, que o responsável aprovou (prompt 3).

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações. A solução inicial foi gravada no commit `829b937` **antes de qualquer revisão**, e a final no commit `093eed1`; o diff está em [`sessao-23-diff-integracao-inicial-final.diff`](sessao-23-diff-integracao-inicial-final.diff).

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| **Commit `829b937`:** fixtures `repo_sqlite`, `repo_memoria` e `repositorio` (parametrizada); `test_servicos_repositorio.py` com 28 casos e `test_contrato_repositorio.py` com 20 casos, total de **48**. `tests/integration`: 76 passed; `ruff` ok. Cobertura de `app.servicos` + `app.repositorios`: **99%** (`auth.py` 94%, linha 27 e 1 ramo não cobertos) | **Commit `093eed1`:** `test_servicos_repositorio.py` com 36 casos, total de **56**. `tests/integration`: **84 passed**. Cobertura: **100%** de linhas e arestas (136 statements, 18 ramos) | Acrescentado `test_registro_invalido_nao_grava_cliente`, parametrizado em nome vazio, e-mail vazio, senha vazia e senha com 5 caracteres, nas duas implementações (+8 casos). O teste confere `CredenciaisInvalidas` e que nenhum cliente foi gravado. Assim, os testes de serviços cobrem as validações do registro sem depender dos testes de rota da #55. O resto da solução inicial ficou sem mudança |

**Decisão:** a solução da IA foi aceita, com o caso de registro inválido acrescentado na revisão. As duas divergências entre as implementações ficaram como comportamento atual fixado em testes, porque o prompt proíbe alterar `app/`. A inconsistência de tipo de `horario` foi registrada na docstring do módulo e no plano de teste.

**Validação inicial:** `uv run pytest tests/integration -q` → `76 passed`; `uv run ruff check tests/integration` → `All checks passed!`; nenhum `banco.db` criado. Validação feita pelo responsável, no terminal dele: `uv run pytest tests/integration -q` → `76 passed`; `uv run pytest` → `628 passed, 2 failed, 3 xfailed`. As 2 falhas são os bugs de PIX #16 e #17, e os 3 `xfail` são do defeito #78. A cobertura com `--cov-branch` deu 99%, com a linha 27 de `auth.py` sem cobertura.

**Validação final:** `uv run pytest tests/integration -v --cov=app.servicos --cov=app.repositorios --cov-branch --cov-report=term-missing --cov-fail-under=0` → `84 passed`, **100%** em todos os arquivos. Evidência: [`servicos-repositorio.txt`](../../relatorios/evidencias/integracao/servicos-repositorio.txt). `ruff` ok; nenhum `banco.db` criado.

## Ações executadas

1. Criada a branch `test/issue-54-integracao-servicos-repositorio` a partir da `main` (`3224ac4`). A branch vazia criada antes, `test/issue-54-integracao-servicos`, foi apagada a pedido do responsável.
2. Lidos repositórios, serviços, `db.py`, `config.py`, `pix.py`, o `conftest.py` e o `test_rotas.py` da #55; linha de base: 28 passed.
3. Plano apresentado e aprovado (prompt 2).
4. Fixtures acrescentadas ao `conftest.py`, sem alterar as da #55; criados os dois arquivos de teste; divergências confirmadas rodando; solução inicial gravada sem revisão (`829b937`).
5. Validação pelo responsável; a IA converteu a evidência de cobertura, gravada pelo PowerShell em UTF-16, para UTF-8, e apontou a linha 27 de `auth.py` sem cobertura.
6. Acrescentado o caso de registro inválido (prompt 3); evidência regravada; versão revisada gravada (`093eed1`).
7. Atualizados `docs/plano_de_teste.md` (v1.18, seção 6.9), o `README.md` e o AI-LOG.

## Resultado

- **56 testes de integração novos**, sem mocks: 36 em `test_servicos_repositorio.py` e 20 em `test_contrato_repositorio.py`. `tests/integration`: **84 passed**.
- Cobertura de `app/servicos` e `app/repositorios` pelos testes de integração: **100%** de linhas e arestas.
- **2 divergências** entre `SqliteRepositorio` e `MemoriaRepositorio` documentadas: e-mail duplicado e `atualizar_saldo` com id inexistente. Há também 1 observação de tipo (`horario`). Nenhum defeito novo e nenhuma alteração em `app/`.
