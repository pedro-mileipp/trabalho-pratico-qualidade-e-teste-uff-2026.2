# Sessão 8 — Caso de teste manual — Auth e Registro (issue #9)

| Campo | Valor |
|---|---|
| Responsável | Gabrielle Rosa (`n2Gabrielle`) |
| Data | 18/09/2026 |
| Ferramenta | VS Code / Terminal / Browser |
| Atividade | Projetar, executar e documentar casos de testes manuais das rotas de autenticação (`/registro`, `/login` e `/logout`) para a issue #9 |
| Artefatos | `tests/testes_manuais/auth/caso_auth.md` + screenshots em `tests/testes_manuais/auth/evidencias/` |

## Contexto

Elaborar a suíte de testes manuais para o módulo de autenticação e registro do Banco Digital. A atividade envolveu subir a aplicação Flask com banco de dados SQLite isolado em `/tmp/teste.db`, exercitar interativamente o fluxo de cadastro, login e encerramento de sessão, avaliar regras de validação nos dados de entrada (como formato de e-mail e tamanho mínimo de senha) e registrar os cenários encontrados e potenciais falhas de usabilidade/UX.

## Prompts utilizados na conversa

> "Pensei nos seguintes casos de teste manuais. 1) tentar logar sem ter uma conta; 2) cadastrar uma conta e logar; 3) clicar em sair para realizar o logout; 4) logar tendo conta já cadastrada; 5) tentar logar com e-mail e senha inválidos; 6) tentar criar outra conta com os mesmos dados já utilizados; 7) tentar não utilizar @; 8) tentar não passar nada depois do @."
>
> "Os testes que fiz foram suficientes?"
>
> "from app.servicos.auth import AuthService... [envio do código de auth.py e auth_service.py para validação da regra de negócio da senha e tratamento de exceções]"

**Resposta da IA — complementação da suíte (2 casos adicionados):**

1. **Análise do código e das rotas**
   - Avaliou o Blueprint de autenticação (`app/blueprints/auth.py`) e o serviço (`app/servicos/auth.py`).
   - Identificou a regra de negócio do backend que exige `len(senha) < 6`, disparando a exceção `CredenciaisInvalidas("senha muito curta")`.
   - Mapeou a causa-raiz da falha de UX: a rota captura `CredenciaisInvalidas` de forma genérica e exibe a mensagem fixa "Dados inválidos. Verifique os campos." quando o problema real é a senha curta.

2. **Revisão da cobertura de testes**
   - Confirmou que os 8 cenários propostos pela usuária cobriam o fluxo principal, mas havia lacunas de borda.
   - Adicionou casos para validar campos vazios e e-mails com formato incompleto em nível de interface e backend.
   - Reforçou a necessidade de verificar se a aplicação mantém a sessão corretamente após logout e se o sistema rejeita duplicidade no cadastro.

## Solução inicial (estrutura pensada) vs. solução final (IA complementando e revisão do que foi gerado)

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| Mapeamento inicial dos cenários de autenticação e registro, focados em login, cadastro e logout | Suíte manual ampliada com 10 cenários executados, incluindo validações de borda e recuperação de fluxo após logout | A IA revisou os casos propostos, identificou lacunas (campos vazios, e-mail incompleto, senha curta) e complementou a suíte com 2 cenários adicionais |

**Decisão:** Os casos iniciais foram mantidos e a suíte foi expandida para cobrir regras de validação e UX do fluxo de autenticação sem alterar a intenção do teste manual.

**Validação:** a execução da interface confirmou que o fluxo principal de cadastro, login e logout funciona e que as regras de e-mail e senha são tratadas de forma consistente.

## Ações executadas

1. Subir a aplicação Flask com banco SQLite isolado em `/tmp/teste.db`.
2. Testar as rotas de `/registro`, `/login` e `/logout` diretamente na interface.
3. Registrar as mensagens exibidas, o comportamento de sessão e os defeitos de validação observados.
4. Revisar a regra de negócio em `app/servicos/auth.py` para complementar a suíte com cenários de borda.

## Resultado

- A suíte executada cobriu 10 cenários, incluindo os 8 propostos pela usuária e 2 adicionais identificados pela IA.
- O fluxo principal de autenticação apresentou comportamento esperado em login, cadastro e logout.
- A validação de e-mail e senha foi consistente com a regra implementada, com destaque para a exigência de senha com pelo menos 6 caracteres.
- Houve apontamento de melhoria de UX em mensagens de erro para entradas inválidas, especialmente quando a senha é curta e a mensagem exibida não distingue claramente o motivo do erro.
