# Sessão 18 — Testes de integração das rotas Flask com test_client

| Campo | Valor |
|---|---|
| Responsável | Vinicius Sales Felinto (`ViniciusFelinto`) |
| Data | 22/11/2026 |
| Ferramenta | Google Antigravity (modelo `Gemini 3.8 Flash`) / Terminal (`uv run pytest`) |
| Atividade | Implementar testes de integração das rotas Flask com `test_client` (Entrega 2) |
| Artefatos | `tests/integration/conftest.py`, `tests/integration/test_rotas.py` |

## Contexto

Atender à exigência de testes de integração da Entrega 2 do trabalho prático. O objetivo é testar a integração real entre as rotas HTTP do Flask (blueprints de autenticação, dashboard, PIX, empréstimo, tarifas e crédito), templates Jinja2, gerenciamento de sessões, mensagens flash, camadas de serviço e repositório SQLite temporário isolado por execução.

## Prompt utilizado

> "Se comporte como um testador experiente com conhecimento nas melhores práticas de teste de software do mercado, tendo em vista isso, preciso que crie testes de integração para o meu projeto seguindo extritamente os requisitos abaixo. Após criar os códigos de teste de integração, me explique o funcionamento e como rodar via terminal
>
> ## Objetivo
> Implementar testes de integração das rotas Flask com `test_client`.
>
> ## Contexto
> - O enunciado exige testes de integração.
> - Usar `create_app` com `TESTING=True` e `DATABASE` temporário.
> - Cobrir os fluxos web principais e as rotas protegidas.
>
> ## O que fazer
> 1. Criar `tests/integration/test_rotas.py` (ou equivalente) usando `app.test_client()`.
> 2. Testar registro → login → dashboard.
> 3. Testar rotas protegidas redirecionando para `/login` sem sessão.
> 4. Testar `POST /pix`: sucesso, valor inválido e recusa, conferindo `flash` e saldo no dashboard.
> 5. Testar `POST /emprestimo`, `/tarifas` e `/credito`, conferindo o resultado exibido.
> 6. Testar logout encerrando a sessão.
>
> ## Critérios de aceite
> - [ ] Testes em `tests/integration/`.
> - [ ] Todas as rotas exercitadas ao menos uma vez.
> - [ ] Banco isolado e limpo entre testes.
> - [ ] `uv run pytest tests/integration -q` verde."

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações quando a IA é usada na geração de testes.

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| Estruturação inicial do arquivo `conftest.py` com fixtures de `app` (banco temporário via `tmp_path`), `cliente`, `cliente_autenticado` e `definir_saldo`, e criação de `test_rotas.py` agrupando classes de teste por fluxo. | Suíte de integração com **28 testes aprovados**, garantindo que todas as 8 rotas e seus métodos GET e POST da aplicação sejam exercitados, com banco isolado e validações estritas de sessão, redirecionamentos e flash messages. | 1. **Separação de Fixtures em `conftest.py`:** Configurada fixture `app` usando `create_app` com `TESTING=True` e SQLite temporário em `tmp_path`, assegurando independência e limpeza entre os testes.<br>2. **Chave PIX válida para validação estrita de CPF:** A regra de domínio em `TransacaoPix._validar_cpf` valida dígitos verificadores reais; utilizou-se o CPF válido `"52998224725"` para garantir sucesso determinístico no teste positivo.<br>3. **Verificação de saldo e extrato no dashboard:** Nos testes de PIX com sucesso, o fluxo segue o redirect para `/` verificando tanto a mensagem de sucesso (`flash`), quanto o saldo decrescido e o lançamento correspondente no extrato HTML.<br>4. **Conformidade de linter (Ruff):** O código foi formatado e inspecionado via `uv run ruff check tests/integration`, com 0 violações apontadas. |

**Decisão:** Centralizar as fixtures reutilizáveis de integração em `tests/integration/conftest.py` e organizar os testes em `tests/integration/test_rotas.py` divididos semanticamente por responsabilidade (Autenticação/Dashboard, Rotas Protegidas, PIX, Serviços Financeiros e Logout).

**Validação inicial e final:**
- Execução: `uv run pytest tests/integration -q` → **28 passed in 20.54s** (100% verde).
- Linting: `uv run ruff check tests/integration` → `All checks passed!`.

## Ações executadas

1. **Inspeção da arquitetura e das rotas:**
   - Leitura de `app/__init__.py`, `app/config.py`, `app/db.py` e todos os blueprints em `app/web/routes/` (`auth.py`, `dashboard.py`, `pix.py`, `emprestimo.py`, `tarifas.py`, `credito.py`).
   - Inspeção dos templates Jinja2 em `app/templates/` para mapear seletores, textos esperados em mensagens `flash`, formatações numéricas e tabelas de extrato.
   - Consulta às regras de validação de CPF e chaves em `app/dominio/pix.py`.

2. **Criação de `tests/integration/conftest.py`:**
   - Fixture `app`: Instancia a aplicação Flask com `TESTING=True`, `SECRET_KEY` própria e `DATABASE = str(tmp_path / "banco_integracao.db")`.
   - Fixture `cliente`: Retorna `app.test_client()` persistindo cookies de sessão.
   - Fixture `cliente_autenticado`: Cadastra e autentica um usuário padrão de integração.
   - Fixture `definir_saldo`: Permite ajustar o saldo do cliente diretamente no banco antes de transações financeiras.

3. **Criação de `tests/integration/test_rotas.py`:**
   - `TestFluxoAutenticacaoEDashboard`: Acesso a `/registro` e `/login` anônimos, fluxo completo registro → dashboard → logout → login, falha por e-mail duplicado, falha por campos vazios e falha por senha incorreta.
   - `TestRotasProtegidasSemSessao`: Parametrização de GET e POST em rotas autenticadas sem sessão (`/`, `/pix`, `/emprestimo`, `/tarifas`, `/credito`), validando redirecionamento 302 para `/login`.
   - `TestRotasPix`: Formulário GET, transferência com sucesso debitando saldo e registrando no extrato, erros de valor não numérico e negativo, recusa por saldo insuficiente e recusa por chave inválida.
   - `TestRotasServicosFinanceiros`: Formulários GET e requisições POST para `/emprestimo` (aprovado e recusado), `/tarifas` (cálculo de tarifa mensal) e `/credito` (situação, score e limite).
   - `TestFluxoLogout`: Encerramento de sessão com purga de `cliente_id` e bloqueio de acessos subsequentes.

4. **Validação da suíte:**
   - Execução automatizada e verificação de critérios de aceite no terminal via `uv run pytest tests/integration -q`.

## Resultado

- **28 testes de integração implementados e aprovados** em `tests/integration/`.
- 100% das rotas e métodos HTTP da aplicação exercitados.
- Isolamento absoluto com banco temporário limpo por teste.
- Suíte 100% verde sem regressões.
