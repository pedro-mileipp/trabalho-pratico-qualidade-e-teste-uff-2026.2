# Relatório — Requisito não funcional de segurança da autenticação (RNF06)

| Campo | Valor |
|---|---|
| Issue | [#61](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/61) |
| Responsável | Pedro Mileipp |
| Requisito | RNF06 — Segurança (autenticação), do [Plano de Teste](../plano_de_teste.md) |
| Característica ISO/IEC 25010:2023 | Segurança |
| Arquivo de testes | [`tests/rnf/seguranca/test_seguranca_autenticacao.py`](../../tests/rnf/seguranca/test_seguranca_autenticacao.py) |
| Data | 11/11/2026 |

## 1. Como os testes foram feitos

Os testes usam o cliente de testes do Flask (`app.test_client()`): fazem requisições HTTP reais às rotas da aplicação, sem navegador. Cada teste recebe uma aplicação nova com o seu próprio banco SQLite temporário (fixtures em [`tests/rnf/conftest.py`](../../tests/rnf/conftest.py)), o que permite também conferir diretamente o que foi gravado no banco.

```bash
uv run pytest tests/rnf/seguranca -v
```

**Resultado:** 22 testes, todos passando (≈ 2,5 s).

## 2. Verificações exigidas pela issue

| # | Verificação | Testes | Casos | Resultado |
|---|---|---|---|---|
| 1 | Acesso direto a rota protegida sem login redireciona para `/login` | `TestAcessoSemLogin` | 11 | ✅ As 5 rotas protegidas (`/`, `/pix`, `/emprestimo`, `/tarifas`, `/credito`) redirecionam no GET e no POST. Um POST sem login não grava nada no banco. `/login` e `/registro` continuam públicas |
| 2 | Depois do logout, rota protegida não mostra dados do cliente | `TestLogout` | 6 | ✅ O logout remove o `cliente_id` da sessão; depois dele, as 5 rotas protegidas levam ao `/login`, sem o nome nem o e-mail do cliente. Ver o risco R1 sobre o botão Voltar do navegador |
| 3 | Senha gravada como hash `pbkdf2:sha256` no banco | `TestArmazenamentoDaSenha` | 2 | ✅ O campo `senha_hash` começa com `pbkdf2:sha256:` (1.000.000 de iterações), não contém a senha e é validado por `check_password_hash`. Dois clientes com a mesma senha têm hashes diferentes (salt por cliente) |
| 4 | Mensagem de erro do login não revela se o e-mail existe | `TestMensagemDeErroDoLogin` | 2 | ✅ E-mail inexistente e senha errada geram respostas idênticas (mesmo status e mesmo HTML: "E-mail ou senha inválidos."). Um login válido abre a sessão |
| — | Cookie de sessão protegido contra leitura por JavaScript | `TestCookieDeSessao` | 1 | ✅ O cookie `session` é enviado com `HttpOnly` |

O item opcional da issue (tempo de resposta das rotas) não foi feito: o enunciado pede pelo menos um requisito não funcional, e a segurança cobre esse ponto.

## 3. Riscos identificados (fora dos critérios da issue)

Durante a investigação, cinco comportamentos chamaram a atenção. Nenhum faz os testes acima falharem, mas eles afetam a característica Segurança e entram na avaliação da ISO 25010. Ficam registrados como riscos conhecidos do sistema, no escopo acadêmico do projeto.

| Id | Risco | Como foi observado | Severidade | Recomendação |
|---|---|---|---|---|
| R1 | Depois do logout, o botão **Voltar** do navegador mostra o painel com o nome e o saldo do cliente | Teste exploratório no Chrome: cadastro → painel → Sair → Voltar. A página volta do cache, porque as telas autenticadas não enviam `Cache-Control: no-store`. Recarregar a página leva ao `/login` | Média (computador compartilhado) | Enviar `Cache-Control: no-store` nas respostas das rotas protegidas |
| R2 | Um cookie de sessão copiado antes do logout continua válido depois dele | Teste exploratório com o cliente de testes: o cookie guardado antes do `/logout` e reenviado depois ainda abre o painel. A sessão do Flask fica toda no cookie assinado, e o logout só apaga o cookie do navegador | Média | Guardar a sessão no servidor (ex.: Flask-Session) ou registrar um identificador de sessão que o logout invalida |
| R3 | `SECRET_KEY` tem um valor padrão fixo no código (`"dev-secret-key"`, em `app/config.py`) | Leitura do código. Se a variável de ambiente `SECRET_KEY` não for definida, qualquer pessoa que conheça esse valor consegue assinar um cookie com o `cliente_id` de outro cliente | Alta, se o sistema for publicado sem a variável | Exigir `SECRET_KEY` por variável de ambiente fora do modo de desenvolvimento |
| R4 | O cadastro revela se um e-mail já existe ("Este e-mail já está cadastrado.") | Teste exploratório: cadastro repetido com o mesmo e-mail | Baixa (enumeração de usuários; o login não revela) | Mensagem genérica no cadastro ou confirmação por e-mail |
| R5 | O cookie de sessão não tem `Secure` nem `SameSite` | Cabeçalho `Set-Cookie: session=...; HttpOnly; Path=/` | Baixa no ambiente local (HTTP) | Em produção: `SESSION_COOKIE_SECURE=True` e `SESSION_COOKIE_SAMESITE="Lax"` |

## 4. Contribuição para a ISO/IEC 25010:2023 — Segurança

Resumo para a avaliação da característica Segurança (issue #62):

| Subcaracterística | Evidência | Situação |
|---|---|---|
| Confidencialidade | Senhas com hash pbkdf2:sha256 e salt; rotas protegidas exigem login; login não revela e-mails cadastrados | Atendida, com os riscos R1, R2 e R4 |
| Integridade | POST sem login não altera dados; cookie de sessão assinado | Atendida, desde que a `SECRET_KEY` não seja a padrão (R3) |
| Não repúdio | Transações registradas no extrato por cliente | Parcial (sem registro de quem fez login, quando) |
| Responsabilização | Não há log de acessos nem de tentativas de login | Não atendida |
| Autenticidade | Login por e-mail e senha; sessão vinculada ao `cliente_id` | Atendida, com os riscos R2 e R3 |
| Resistência | Sem limite de tentativas de login nem bloqueio de conta | Não avaliada por testes |
