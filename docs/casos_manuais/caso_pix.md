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
| Técnica aplicada | Partição de equivalência + análise de valor-limite (fronteiras de saldo, limite e horário) |

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
5. Confirmar saldo no dashboard (`/`) e acessar `/pix`.

### Dados de teste

| Dado | Valor | Classificação |
|---|---|---|
| CPF válido | `529.982.247-25` | entrada válida |
| CPF inválido | `123.456.789-00` | entrada inválida |
| E-mail válido | `pix@teste.com` | entrada válida |
| E-mail com dois `@` | `a@b@c.com` | entrada inválida (provável defeito #16) |
| Telefone válido (11 dígitos) | `(21) 99999-9999` | entrada válida |
| Chave aleatória (32 chars) | `99999999999999999999999999999999` | entrada válida |
| Chave aleatória (31 chars) | `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | entrada inválida |

## 3. Casos de teste executados

> Limites PIX (configuração padrão): diurno R$ 5.000,00 (06h–20h) e noturno R$ 1.000,00 (20h–06h). Execução ocorreu em período **noturno** (limite de R$ 1.000,00).

| ID | Cenário | Pré-condição | Passos | Dados de entrada | Resultado esperado | Resultado obtido | Status | Evidência |
|---|---|---|---|---|---|---|---|---|
| TC-01 | PIX válido com chave CPF | Conta logada, saldo R$ 10.000,00 | 1) Acessar `/pix`; 2) preencher chave, tipo e valor; 3) enviar | chave `529.982.247-25` (cpf), valor `100.00` | Sucesso: redireciona ao dashboard, flash "Transferência realizada com sucesso.", saldo R$ 9.900,00 e extrato com `PIX cpf -100,00` | Sucesso: redirecionado ao dashboard com a mensagem; saldo R$ 9.900,00; extrato `PIX cpf R$ -100,00` | PASS | `tc01-pix-cpf-valido.png`, `tc01-extrato-apos-pix.png` |
| TC-02 | Fronteira: valor igual ao saldo | Conta logada, saldo R$ 100,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave `529.982.247-25` (cpf), valor `100.00` | Sucesso com saldo final R$ 0,00 | Sucesso; saldo final R$ 0,00 | PASS | `tc02-valor-igual-saldo.png` |
| TC-03 | Chave CPF inválida | Conta logada, saldo R$ 10.000,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave `123.456.789-00` (cpf), valor `50.00` | Mensagem "Chave PIX inválida.", permanece em `/pix`, saldo intacto | Mensagem "Chave PIX inválida." em `/pix`; saldo intacto | PASS | `tc03-cpf-invalido.png` |
| TC-04 | Chave aleatória com tamanho inválido (31 chars) | Conta logada | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave de 31 caracteres (aleatoria), valor `50.00` | Mensagem "Chave PIX inválida.", saldo intacto | Mensagem "Chave PIX inválida."; saldo intacto | PASS | `tc04-aletoria-31-char.png` |
| TC-05 | Valor inválido (zero) | Conta logada | 1) Acessar `/pix`; 2) preencher chave/tipo e valor `0`; 3) enviar | chave `529.982.247-25` (cpf), valor `0` | Bloqueio na camada de apresentação: `min="0.01"` do HTML5 impede o envio (mensagem nativa do navegador) | Formulário não submetido (permanece em `/pix`, sem flash e sem débito); mensagem de validação nativa do navegador | PASS | `tc05-valor-zero-html5.png` |
| TC-06 | Valor acima do limite noturno (executado às 22h) | Conta logada, saldo R$ 10.000,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave `529.982.247-25` (cpf), valor `1500.00` | Período noturno: "Operação fora do horário permitido." (limite R$ 1.000,00), saldo intacto | Mensagem "Operação fora do horário permitido."; saldo intacto | PASS | `tc06-acima-limite-noturno.png` |
| TC-07 | Saldo insuficiente | Conta logada, saldo R$ 100,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave `529.982.247-25` (cpf), valor `500.00` | Mensagem "Saldo insuficiente.", saldo intacto | Mensagem "Saldo insuficiente."; saldo intacto | PASS | `tc07-saldo-insuficiente.png` |
| TC-08 | Acesso a `/pix` sem autenticação | Navegador sem sessão | 1) Acessar `/pix` diretamente | — | Redirecionamento para `/login` | Redirecionado para `/login` | PASS | `tc08-pix-sem-login-redirect.png` |
| TC-09 | PIX válido com chave e-mail | Conta logada, saldo R$ 10.000,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave `pix@teste.com` (email), valor `50.00` | Sucesso; saldo R$ 9.950,00 | Sucesso; saldo R$ 9.950,00 | PASS | `tc09-email-valido.png` |
| TC-10 | PIX válido com chave telefone (11 dígitos) | Conta logada, saldo R$ 10.000,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave `(21) 99999-9999` (telefone), valor `30.00` | Sucesso; saldo R$ 9.970,00 | Sucesso; saldo R$ 9.970,00 | PASS | `tc10-telefone-valido.png` |
| TC-11 | PIX válido com chave aleatória (32 chars) | Conta logada, saldo R$ 10.000,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave de 32 caracteres (aleatoria), valor `20.00` | Sucesso; saldo R$ 9.980,00 | Sucesso; saldo R$ 9.980,00 | PASS | `tc11-aletoria-32-char.png` |
| TC-12 | Chave e-mail com dois `@` (defeito #16) | Conta logada, saldo R$ 10.000,00 | 1) Acessar `/pix`; 2) preencher; 3) enviar | chave `a@b@c.com` (email), valor `25.00` | Chave inválida → "Chave PIX inválida.", saldo intacto | **Sucesso indevido**: transferência aceita, saldo R$ 9.975,00 | **FAIL** | `tc12-email-dois-arroba-DEFEITO16.png` |

## 4. Defeitos encontrados

| ID | Descrição | Severidade | Vínculo |
|---|---|---|---|
| TC-12 | Chave e-mail com dois `@` (`a@b@c.com`) é aceita como válida e o PIX é debitado. O esperado é a rejeição da chave. | Média | [#16 — e-mail com dois '@' aceito como válido](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/16) |

## 5. Observações

- **TC-05 (valor ≤ 0):** a validação é feita pelo HTML5 (`min="0.01"`) antes de chegar ao servidor. O backend também trata valores inválidos (flash "Valor inválido." em `/pix`), mas esse caminho só é alcançado contornando a validação do navegador.
- **TC-06 (limite):** o resultado depende do horário de execução. Às 22h (noturno, limite R$ 1.000,00) retornou "Operação fora do horário permitido.". O cenário diurno (valor > R$ 5.000,00 → "Valor acima do limite permitido.") deve ser executado entre 06h e 20h para ser reproduzido.
- **Chave bloqueada:** não é testável pela UI na configuração padrão (lista `chaves_bloqueadas` vazia e sem configuração via web). É coberta pelos testes unitários de `TransacaoPix`.
- **Extrato:** a tabela de extrato acumula todas as transações da sessão de teste; o saldo foi reajustado via SQLite entre os casos que dependem de saldo.

## 6. Conclusão

- Executados **12 casos**: **11 PASS** e **1 FAIL** (TC-12).
- O caso com falha confirma o defeito conhecido **#16** (e-mail com dois `@` aceito como válido), já registrado como issue no GitHub.
- Nenhuma falha crítica foi encontrada nos fluxos de sucesso, validação de chaves, saldo e autenticação.