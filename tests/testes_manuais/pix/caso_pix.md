# Caso de Teste Manual — Transferência PIX

> Documento da issue **#8** — caso de teste manual da funcionalidade PIX do Banco Digital.

## 1. Identificação

| Campo | Valor |
|---|---|
| Funcionalidade | PIX — Transferência (`/pix`) |
| Issue | [#8](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/8) |
| Executor | Alexandre Colmenero |
| Data de execução | 16/09/2026, ~22h03 (período noturno do PIX: 20h–6h) |
| Ambiente | macOS · Google Chrome (headless) · `DATABASE=/tmp/pix_teste.db` |
| Build testado | commit `a31c991` (main) |
| Técnica aplicada | Partição de equivalência + análise de valor-limite |

## 2. Pré-condições e preparação

1. `uv sync --all-extras`
2. Subir a aplicação com banco fora do workspace (evita criar `banco.db`):
   ```bash
   DATABASE=/tmp/pix_teste.db uv run flask --app app:create_app run
   ```
3. Criar conta em `http://127.0.0.1:5000/registro`:
   - Nome: `Teste PIX`
   - E-mail: `pix@teste.com`
   - Senha: `senha123`
4. **Ajustar saldo via SQLite** (a aplicação não possui depósito pela UI e a conta nasce com saldo `0`):
   ```bash
   sqlite3 /tmp/pix_teste.db "UPDATE clientes SET saldo = 10000 WHERE email = 'pix@teste.com';"
   ```
5. Confirmar saldo no dashboard (`/`) — evidência em `evidencias/setup-dashboard-saldo-10000.png` — e acessar `/pix`.

### Dados de teste

| Dado | Valor | Classificação |
|---|---|---|
| CPF válido | `529.982.247-25` | entrada válida |
| CPF inválido | `123.456.789-00` | entrada inválida |
| E-mail com dois `@` | `a@b@c.com` | entrada inválida (defeito #16) |

## 3. Casos de teste executados

> A execução na interface cobriu 12 cenários (válidos e inválidos). Por decisão de escopo, este documento registra os **4 casos representativos**: fluxo válido, chave inválida, saldo insuficiente e o defeito conhecido de e-mail.

| ID | Cenário | Pré-condição | Passos | Dados de entrada | Resultado esperado | Resultado obtido | Status | Evidência |
|---|---|---|---|---|---|---|---|---|
| TC-01 | PIX válido com chave CPF | Conta logada, saldo R$ 10.000,00 | 1) Acessar `/pix`; 2) preencher chave, tipo e valor; 3) enviar | chave `529.982.247-25` (cpf), valor `100.00` | Sucesso: redireciona ao dashboard, flash "Transferência realizada com sucesso.", saldo R$ 9.900,00 e extrato com `PIX cpf -100,00` | Sucesso: redirecionado ao dashboard com a mensagem; saldo R$ 9.900,00; extrato `PIX cpf R$ -100,00` | PASS | `evidencias/tc01-pix-cpf-valido.png`, `evidencias/tc01-extrato-apos-pix.png` |
| TC-02 | Chave CPF inválida | Conta logada, saldo R$ 10.000,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave `123.456.789-00` (cpf), valor `50.00` | Mensagem "Chave PIX inválida.", permanece em `/pix`, saldo intacto | Mensagem "Chave PIX inválida." em `/pix`; saldo intacto | PASS | `evidencias/tc02-cpf-invalido.png` |
| TC-03 | Saldo insuficiente | Conta logada, saldo R$ 100,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave `529.982.247-25` (cpf), valor `500.00` | Mensagem "Saldo insuficiente.", saldo intacto | Mensagem "Saldo insuficiente."; saldo intacto | PASS | `evidencias/tc03-saldo-insuficiente.png` |
| TC-04 | Chave e-mail com dois `@` (defeito #16) | Conta logada, saldo R$ 10.000,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave `a@b@c.com` (email), valor `25.00` | Chave inválida → "Chave PIX inválida.", saldo intacto | **Sucesso indevido**: transferência aceita, saldo R$ 9.975,00 | **FAIL** | `evidencias/tc04-email-dois-arroba-DEFEITO16.png` |

## 4. Defeitos encontrados

| ID | Descrição | Severidade | Vínculo |
|---|---|---|---|
| TC-04 | Chave e-mail com dois `@` (`a@b@c.com`) é aceita como válida e o PIX é debitado. O esperado é a rejeição da chave. | Média | [#16 — e-mail com dois '@' aceito como válido](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/16) |

## 5. Observações

- **Valor ≤ 0:** barrado pelo HTML5 (`min="0.01"`) antes de chegar ao servidor; o backend também trata o caso (flash "Valor inválido.").
- **Limite por horário:** a execução ocorreu às 22h (período noturno, limite R$ 1.000,00). Cenários de limite e de chave bloqueada são cobertos pelos testes unitários de `TransacaoPix`.
- **Extrato:** a tabela de extrato acumula as transações da sessão de teste; o saldo foi reajustado via SQLite entre os casos que dependem de saldo.

## 6. Conclusão

- Executados **4 casos**: **3 PASS** e **1 FAIL** (TC-04).
- O caso com falha confirma o defeito conhecido **#16** (e-mail com dois `@` aceito como válido), já registrado como issue no GitHub.
- Os fluxos de sucesso, validação de chaves e saldo funcionaram conforme o esperado.