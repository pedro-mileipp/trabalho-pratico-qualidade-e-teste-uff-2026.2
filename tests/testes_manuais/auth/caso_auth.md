# Caso de Teste Manual — Autenticação e Registro

> Documento da issue **#9** — caso de teste manual das funcionalidades de cadastro, login e logout do Banco Digital.

## 1. Identificação

| Campo | Valor |
|---|---|
| Funcionalidade | Autenticação (`/registro`, `/login` e `/logout`) |
| Issue | [#9](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/9) |
| Executor | Gabrielle Rosa |
| Data de execução | 18/09/2026 |
| Ambiente | Linux (Ubuntu) · Google Chrome · `DATABASE=/tmp/teste.db` |
| Build testado | commit `main` |
| Técnica aplicada | Partição de equivalência + análise de valor-limite |

## 2. Pré-condições e preparação

1. Subir a aplicação Flask com banco SQLite isolado em `/tmp/teste.db` para não poluir o workspace:
   ```bash
   DATABASE=/tmp/teste.db uv run flask --app app:create_app run
   ```
2. Acessar `http://127.0.0.1:5000/` no navegador.
3. Garantir acesso às telas de `/login` e `/registro`.

### Dados de teste

| Dado | Valor | Classificação |
|---|---|---|
| Nome válido | `Gabrielle Rosa` | entrada válida |
| E-mail válido | `gabrielle@teste.com` | entrada válida |
| Senha válida | `senha123` (≥ 6 caracteres) | entrada válida |
| Senha curta | `12345` (< 6 caracteres) | entrada inválida |
| E-mail sem `@` | `gabrielle.com` | entrada inválida (HTML5) |
| E-mail sem domínio | `gabrielle@` | entrada inválida (HTML5) |

## 3. Casos de teste executados

A execução na interface cobriu 11 cenários (válidos e inválidos). O escopo inclui os 9 cenários propostos originalmente pela usuária e 2 cenários adicionados pela IA para cobertura de borda.

| ID | Cenário | Origem | Pré-condição | Passos | Dados de entrada | Resultado esperado | Resultado obtido | Status | Evidência |
|---|---|---|---|---|---|---|---|---|---|
| CT-01 | Login com usuário inexistente | Proposto pela usuária | Nenhuma conta cadastrada | 1) Acessar `/login`; 2) preencher e-mail e senha; 3) enviar | e-mail inexistente `teste@inexistente.com`, senha `123456` | Exibir mensagem de erro: "E-mail ou senha inválidos." | Mensagem "E-mail ou senha inválidos." exibida em `/login` | PASS | `evidencias/ct01-login-usuario-inexistente.png` |
| CT-02 | Cadastro e login com sucesso | Proposto pela usuária | Nenhuma conta cadastrada com o e-mail | 1) Acessar `/registro`; 2) preencher dados válidos; 3) enviar | nome `Gabrielle Rosa`, e-mail `gabrielle@teste.com`, senha `senha123` | Criar conta e redirecionar para a dashboard com mensagem de sucesso | Conta criada e redirecionado para a Dashboard com exibição do saldo | PASS | `evidencias/ct02-cadastro-login-sucesso.png` |
| CT-03 | Encerrar sessão (Logout) | Proposto pela usuária | Usuário autenticado na Dashboard | 1) Clicar no botão "Sair" no menu superior | N/A | Encerrar sessão e redirecionar para `/login` | Redirecionado para `/login` com a sessão encerrada | PASS | `evidencias/ct03-logout-sucesso.png` |
| CT-04 | Reautenticação após logout | Proposto pela usuária | Conta já cadastrada | 1) Acessar `/login`; 2) preencher credenciais recém-criadas; 3) enviar | e-mail `gabrielle@teste.com`, senha `senha123` | Acesso concedido e redirecionamento para a Dashboard | Redirecionado para a Dashboard com saldo exibido | PASS | `evidencias/ct04-relogin-sucesso.png` |
| CT-05 | Login com e-mail e senha inválidos | Proposto pela usuária | Conta cadastrada no passo CT-02 | 1) Acessar `/login`; 2) informar e-mail/senha incorretos; 3) enviar | e-mail `gabrielle@teste.com`, senha `senhaERRADA` | Bloquear acesso e exibir erro de autenticação | Mensagem de erro exibida e permanência em `/login` | PASS | `evidencias/ct05-login-invalido.png` |
| CT-06 | Cadastro com e-mail e senha inválidos | Proposto pela usuária | Nenhuma conta com o e-mail informado | 1) Acessar `/registro`; 2) preencher dados; 3) enviar | e-mail `gabrielle@teste.com`, senha `12345` | Rejeitar cadastro e indicar dados inválidos | Cadastro bloqueado e mensagem de erro exibida | PASS | `evidencias/ct06-cadastro-invalidos.png` |
| CT-07 | Tentativa de cadastro duplicado | Proposto pela usuária | Conta já cadastrada | 1) Acessar `/registro`; 2) repetir dados existentes; 3) enviar | nome `Gabrielle Rosa`, e-mail `gabrielle@teste.com`, senha `senha123` | Rejeitar cadastro por e-mail duplicado | Sistema rejeitou a criação de conta duplicada | PASS | `evidencias/ct07-cadastro-duplicado.png` |
| CT-08 | E-mail sem `@` | Proposto pela usuária | Sem conta com o e-mail informado | 1) Acessar `/registro`; 2) preencher formulário; 3) enviar | e-mail `gabrielle.com`, senha `senha123` | Invalidar campo e não criar conta | Validação de entrada bloqueou o cadastro | PASS | `evidencias/ct08-email-sem-arroba.png` |
| CT-09 | E-mail sem domínio | Proposto pela usuária | Sem conta com o e-mail informado | 1) Acessar `/registro`; 2) preencher formulário; 3) enviar | e-mail `gabrielle@`, senha `senha123` | Invalidar campo e não criar conta | Validação do HTML5/cliente bloqueou a ação | PASS | `evidencias/ct09-email-sem-dominio.png` |
| CT-10 | Senha curta | Adicionado pela IA | Sem conta com o e-mail informado | 1) Acessar `/registro`; 2) preencher senha com 5 caracteres; 3) enviar | e-mail `novo@teste.com`, senha `12345` | Rejeitar cadastro com mensagem de senha curta | Exibida mensagem de dados inválidos; conta não criada | PASS | `evidencias/ct10-senha-curta.png` |
| CT-11 | Campos vazios em formulário de cadastro | Adicionado pela IA | Tela de registro acessível | 1) Acessar `/registro`; 2) enviar sem preencher campos | nome vazio, e-mail vazio, senha vazia | Validar obrigatório antes do envio e impedir cadastro | Formulário bloqueou submissão com validação de campos vazios | PASS | `evidencias/ct11-campos-vazios.png` |

## 4. Defeitos e observações

- O fluxo principal de autenticação atende ao esperado para cadastro, login e logout.
- A regra de senha mínima de 6 caracteres foi validada corretamente no backend e na interface.
- A mensagem de erro para senha curta é genérica e pode ser melhorada em UX, para indicar com precisão que o motivo é a senha curta.
- O formulário de cadastro impede entradas inválidas com validação do browser e do backend, reduzindo possibilidade de dados inconsistentes.

## 5. Conclusão

Os testes manuais realizados para a funcionalidade de autenticação e registro cobriram o fluxo principal e os cenários de borda relevantes. O comportamento observado foi consistente com os requisitos da issue #9, e a área principal de melhoria apontada foi a clareza da mensagem de erro para senhas curtas.
