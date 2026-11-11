"""Requisito não funcional de segurança da autenticação — RNF06, issue #61.

Verificações (a mesma ordem da issue):
1. rotas protegidas exigem login;
2. depois do logout, as rotas protegidas não mostram dados do cliente;
3. a senha é gravada como hash pbkdf2:sha256, com salt;
4. a mensagem de erro do login não revela se o e-mail existe.
Mais: o cookie de sessão é HttpOnly.

Resultados e riscos encontrados fora destes critérios: docs/relatorios/rnf_seguranca.md.
"""

from __future__ import annotations

import pytest
from werkzeug.security import check_password_hash

ROTAS_PROTEGIDAS = ["/", "/pix", "/emprestimo", "/tarifas", "/credito"]
DADOS_CADASTRO = {"nome": "Outro Cliente", "senha": "outra-senha-456"}


class TestAcessoSemLogin:
    @pytest.mark.parametrize("rota", ROTAS_PROTEGIDAS)
    def test_get_em_rota_protegida_redireciona_para_login(self, cliente_http, rota):
        resposta = cliente_http.get(rota)

        assert resposta.status_code == 302
        assert resposta.headers["Location"] == "/login"

    @pytest.mark.parametrize("rota", ["/pix", "/emprestimo", "/tarifas", "/credito"])
    def test_post_em_rota_protegida_redireciona_sem_processar(self, cliente_http, banco, rota):
        resposta = cliente_http.post(rota, data={"chave": "a@b.com", "valor": "100", "renda": "5000"})

        assert resposta.status_code == 302
        assert resposta.headers["Location"] == "/login"
        assert banco.execute("SELECT COUNT(*) FROM transacoes").fetchone()[0] == 0

    @pytest.mark.parametrize("rota", ["/login", "/registro"])
    def test_telas_publicas_continuam_acessiveis(self, cliente_http, rota):
        assert cliente_http.get(rota).status_code == 200


class TestLogout:
    def test_logout_encerra_a_sessao(self, cliente_http, cliente_cadastrado):
        assert cliente_http.get("/").status_code == 200  # logado antes do logout

        resposta = cliente_http.get("/logout")

        assert resposta.status_code == 302
        assert resposta.headers["Location"] == "/login"
        with cliente_http.session_transaction() as sessao:
            assert "cliente_id" not in sessao

    @pytest.mark.parametrize("rota", ROTAS_PROTEGIDAS)
    def test_apos_logout_rota_protegida_nao_mostra_dados(self, cliente_http, cliente_cadastrado, rota):
        cliente_http.get("/logout")

        resposta = cliente_http.get(rota, follow_redirects=True)

        corpo = resposta.get_data(as_text=True)
        assert resposta.request.path == "/login"
        assert cliente_cadastrado["nome"] not in corpo
        assert cliente_cadastrado["email"] not in corpo


class TestArmazenamentoDaSenha:
    def test_senha_gravada_como_hash_pbkdf2_sha256(self, cliente_cadastrado, banco):
        (senha_hash,) = banco.execute(
            "SELECT senha_hash FROM clientes WHERE email = ?", (cliente_cadastrado["email"],)
        ).fetchone()

        assert senha_hash.startswith("pbkdf2:sha256:")
        assert cliente_cadastrado["senha"] not in senha_hash
        assert check_password_hash(senha_hash, cliente_cadastrado["senha"])

    def test_mesma_senha_gera_hashes_diferentes(self, app, banco):
        for email in ("primeiro@teste.com", "segundo@teste.com"):
            app.test_client().post("/registro", data={**DADOS_CADASTRO, "email": email})

        hashes = [linha[0] for linha in banco.execute("SELECT senha_hash FROM clientes")]

        assert len(hashes) == 2
        assert hashes[0] != hashes[1]  # salt diferente por cliente


class TestMensagemDeErroDoLogin:
    def test_email_inexistente_e_senha_errada_tem_a_mesma_resposta(self, app, cliente_cadastrado):
        visitante = app.test_client()

        email_inexistente = visitante.post(
            "/login", data={"email": "nao.existe@teste.com", "senha": cliente_cadastrado["senha"]}
        )
        senha_errada = visitante.post(
            "/login", data={"email": cliente_cadastrado["email"], "senha": "senha-errada-999"}
        )

        assert email_inexistente.status_code == senha_errada.status_code == 200
        assert email_inexistente.data == senha_errada.data
        assert "E-mail ou senha inválidos." in email_inexistente.get_data(as_text=True)

    def test_login_valido_abre_a_sessao(self, app, cliente_cadastrado):
        visitante = app.test_client()

        resposta = visitante.post(
            "/login", data={"email": cliente_cadastrado["email"], "senha": cliente_cadastrado["senha"]}
        )

        assert resposta.status_code == 302
        assert resposta.headers["Location"] == "/"
        assert cliente_cadastrado["nome"] in visitante.get("/").get_data(as_text=True)


class TestCookieDeSessao:
    def test_cookie_de_sessao_e_httponly(self, cliente_http):
        resposta = cliente_http.post("/registro", data={**DADOS_CADASTRO, "email": "cookie@teste.com"})

        assert "HttpOnly" in resposta.headers["Set-Cookie"]
