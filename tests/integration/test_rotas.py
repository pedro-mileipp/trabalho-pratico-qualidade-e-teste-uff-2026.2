"""Testes de integração das rotas Flask da aplicação Banco Digital.

Verifica a integração entre a camada web (Flask blueprints, templates, sessões, flash messages),
a camada de serviços, a camada de domínio e a persistência em banco SQLite temporário.

Critérios cobertos:
1. Registro -> Login -> Dashboard.
2. Rotas protegidas redirecionando para /login sem sessão ativa.
3. POST /pix: sucesso, valor inválido e recusa, conferindo flash messages e saldo no dashboard.
4. POST /emprestimo, /tarifas e /credito, conferindo resultados exibidos.
5. Logout encerrando a sessão do cliente.
"""

from __future__ import annotations

import pytest
from flask.testing import FlaskClient

ROTAS_PROTEGIDAS = ["/", "/pix", "/emprestimo", "/tarifas", "/credito"]


class TestFluxoAutenticacaoEDashboard:
    """Testa o fluxo completo de registro, login, acesso ao dashboard e validações de auth."""

    def test_telas_publicas_sao_acessiveis_sem_sessao(self, cliente: FlaskClient) -> None:
        """As telas de cadastro e autenticação devem responder com HTTP 200 para usuários anônimos."""
        resp_registro = cliente.get("/registro")
        assert resp_registro.status_code == 200
        assert "Criar conta" in resp_registro.get_data(as_text=True)

        resp_login = cliente.get("/login")
        assert resp_login.status_code == 200
        assert "Entrar" in resp_login.get_data(as_text=True)

    def test_fluxo_completo_registro_login_dashboard(self, cliente: FlaskClient) -> None:
        """Cenário principal: registrar novo cliente, acessar dashboard, sair e logar novamente."""
        dados_cadastro = {
            "nome": "Mariana Ferreira",
            "email": "mariana@bancodigital.com",
            "senha": "senha-segura-mariana",
        }

        # 1. Registro
        resposta_registro = cliente.post("/registro", data=dados_cadastro, follow_redirects=False)
        assert resposta_registro.status_code == 302
        assert resposta_registro.headers["Location"] == "/"

        # 2. Acesso imediato ao Dashboard via sessão criada no registro
        resposta_dashboard = cliente.get("/")
        assert resposta_dashboard.status_code == 200
        corpo_dashboard = resposta_dashboard.get_data(as_text=True)
        assert "Olá, Mariana Ferreira!" in corpo_dashboard
        assert "Saldo:</strong> R$ 0.00" in corpo_dashboard
        assert "Score:</strong> 500" in corpo_dashboard
        assert "Nenhuma transação." in corpo_dashboard

        # 3. Logout para encerrar sessão
        resposta_logout = cliente.get("/logout")
        assert resposta_logout.status_code == 302
        assert resposta_logout.headers["Location"] == "/login"

        # 4. Login com as credenciais cadastradas
        resposta_login = cliente.post(
            "/login",
            data={"email": dados_cadastro["email"], "senha": dados_cadastro["senha"]},
            follow_redirects=False,
        )
        assert resposta_login.status_code == 302
        assert resposta_login.headers["Location"] == "/"

        # 5. Dashboard após autenticação
        resposta_dashboard_pos_login = cliente.get("/")
        assert resposta_dashboard_pos_login.status_code == 200
        assert "Olá, Mariana Ferreira!" in resposta_dashboard_pos_login.get_data(as_text=True)

    def test_registro_falha_quando_email_ja_cadastrado(
        self, cliente: FlaskClient, cliente_autenticado: dict[str, str | int]
    ) -> None:
        """Tentativa de cadastrar e-mail já existente deve renderizar aviso e manter status 200."""
        resposta = cliente.post(
            "/registro",
            data={
                "nome": "Clone",
                "email": cliente_autenticado["email"],
                "senha": "qualquer-senha",
            },
        )
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "Este e-mail já está cadastrado." in corpo

    def test_registro_falha_com_campos_invalidos(self, cliente: FlaskClient) -> None:
        """Campos vazios ou inválidos no cadastro devem exibir mensagem informativa de erro."""
        resposta = cliente.post(
            "/registro",
            data={"nome": "", "email": "", "senha": ""},
        )
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "Dados inválidos. Verifique os campos." in corpo

    def test_login_falha_com_senha_incorreta(
        self, cliente: FlaskClient, cliente_autenticado: dict[str, str | int]
    ) -> None:
        """Tentativa de login com senha incorreta deve exibir mensagem sem autenticar."""
        # Desloga antes de tentar autenticar com senha incorreta
        cliente.get("/logout")

        resposta = cliente.post(
            "/login",
            data={"email": cliente_autenticado["email"], "senha": "senha-incorreta"},
        )
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "E-mail ou senha inválidos." in corpo


class TestRotasProtegidasSemSessao:
    """Garante que requisições sem sessão válida sejam interceptadas e redirecionadas para /login."""

    @pytest.mark.parametrize("rota", ROTAS_PROTEGIDAS)
    def test_get_em_rotas_protegidas_redireciona_para_login(
        self, cliente: FlaskClient, rota: str
    ) -> None:
        """Requisições GET em endpoints autenticados devem retornar 302 para /login."""
        resposta = cliente.get(rota, follow_redirects=False)
        assert resposta.status_code == 302
        assert resposta.headers["Location"] == "/login"

        # Seguindo o redirecionamento, a tela de login deve ser exibida
        resposta_redirecionada = cliente.get(rota, follow_redirects=True)
        assert resposta_redirecionada.status_code == 200
        assert "Entrar" in resposta_redirecionada.get_data(as_text=True)

    @pytest.mark.parametrize("rota", ["/pix", "/emprestimo", "/tarifas", "/credito"])
    def test_post_em_rotas_protegidas_redireciona_para_login(
        self, cliente: FlaskClient, rota: str
    ) -> None:
        """Requisições POST não autorizadas devem ser bloqueadas com 302 para /login."""
        resposta = cliente.post(
            rota,
            data={"qualquer_campo": "qualquer_valor"},
            follow_redirects=False,
        )
        assert resposta.status_code == 302
        assert resposta.headers["Location"] == "/login"


class TestRotasPix:
    """Testa a integração da rota /pix: sucesso, erros de entrada, recusas e impactos no dashboard."""

    def test_get_pix_autenticado_exibe_formulario(
        self, cliente: FlaskClient, cliente_autenticado: dict[str, str | int]
    ) -> None:
        """Cliente autenticado deve acessar o formulário de transferência PIX."""
        resposta = cliente.get("/pix")
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "Transferência PIX" in corpo
        assert "Chave" in corpo

    def test_pix_sucesso_atualiza_saldo_e_reflete_no_dashboard(
        self,
        cliente: FlaskClient,
        cliente_autenticado: dict[str, str | int],
        definir_saldo,
    ) -> None:
        """Transferência com saldo suficiente deve redirecionar para o dashboard com extrato e saldo reduzido."""
        cliente_id = int(cliente_autenticado["id"])
        definir_saldo(cliente_id, 800.0)

        # CPF válido conhecido que atende aos dígitos verificadores do domínio
        cpf_destino_valido = "52998224725"
        valor_transferencia = 250.0

        resposta = cliente.post(
            "/pix",
            data={"chave": cpf_destino_valido, "tipo": "cpf", "valor": str(valor_transferencia)},
            follow_redirects=False,
        )
        assert resposta.status_code == 302
        assert resposta.headers["Location"] == "/"

        # Checa a exibição da mensagem de sucesso e novo saldo no dashboard
        resposta_dashboard = cliente.get("/")
        assert resposta_dashboard.status_code == 200
        corpo_dashboard = resposta_dashboard.get_data(as_text=True)
        assert "Transferência realizada com sucesso." in corpo_dashboard
        assert "Saldo:</strong> R$ 550.00" in corpo_dashboard
        assert "PIX cpf" in corpo_dashboard
        assert "R$ -250.00" in corpo_dashboard

    def test_pix_falha_com_valor_invalido_texto(
        self,
        cliente: FlaskClient,
        cliente_autenticado: dict[str, str | int],
        definir_saldo,
    ) -> None:
        """Entrada de valor não numérico deve retornar erro amigável e manter o saldo inalterado."""
        cliente_id = int(cliente_autenticado["id"])
        definir_saldo(cliente_id, 500.0)

        resposta = cliente.post(
            "/pix",
            data={"chave": "52998224725", "tipo": "cpf", "valor": "invalido"},
        )
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "Valor inválido." in corpo

        # Verifica que o saldo não foi alterado
        corpo_dashboard = cliente.get("/").get_data(as_text=True)
        assert "Saldo:</strong> R$ 500.00" in corpo_dashboard

    def test_pix_falha_com_valor_negativo_ou_zero(
        self,
        cliente: FlaskClient,
        cliente_autenticado: dict[str, str | int],
        definir_saldo,
    ) -> None:
        """Valores negativos ou zero devem ser rejeitados e manter o saldo intacto."""
        cliente_id = int(cliente_autenticado["id"])
        definir_saldo(cliente_id, 300.0)

        resposta = cliente.post(
            "/pix",
            data={"chave": "52998224725", "tipo": "cpf", "valor": "-20.00"},
        )
        assert resposta.status_code == 200
        assert "Valor inválido." in resposta.get_data(as_text=True)

        corpo_dashboard = cliente.get("/").get_data(as_text=True)
        assert "Saldo:</strong> R$ 300.00" in corpo_dashboard

    def test_pix_recusa_por_saldo_insuficiente(
        self,
        cliente: FlaskClient,
        cliente_autenticado: dict[str, str | int],
        definir_saldo,
    ) -> None:
        """Transferência com valor superior ao saldo disponível deve ser recusada."""
        cliente_id = int(cliente_autenticado["id"])
        definir_saldo(cliente_id, 75.0)

        resposta = cliente.post(
            "/pix",
            data={"chave": "52998224725", "tipo": "cpf", "valor": "200.00"},
        )
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "Saldo insuficiente." in corpo

        # Garante que nenhuma quantia foi debitada
        corpo_dashboard = cliente.get("/").get_data(as_text=True)
        assert "Saldo:</strong> R$ 75.00" in corpo_dashboard
        assert "Nenhuma transação." in corpo_dashboard

    def test_pix_recusa_por_chave_invalida(
        self,
        cliente: FlaskClient,
        cliente_autenticado: dict[str, str | int],
        definir_saldo,
    ) -> None:
        """Chave com formato incorreto deve ser recusada com a devida mensagem flash."""
        cliente_id = int(cliente_autenticado["id"])
        definir_saldo(cliente_id, 400.0)

        resposta = cliente.post(
            "/pix",
            data={"chave": "11111111111", "tipo": "cpf", "valor": "50.00"},
        )
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "Chave PIX inválida." in corpo

        corpo_dashboard = cliente.get("/").get_data(as_text=True)
        assert "Saldo:</strong> R$ 400.00" in corpo_dashboard


class TestRotasServicosFinanceiros:
    """Testa os formulários e processamentos de /emprestimo, /tarifas e /credito."""

    @pytest.mark.parametrize(
        ("rota", "titulo_esperado"),
        [
            ("/emprestimo", "Simulação de Empréstimo"),
            ("/tarifas", "Consulta de Tarifas"),
            ("/credito", "Análise de Crédito"),
        ],
    )
    def test_get_telas_de_servicos_exibem_formularios(
        self,
        cliente: FlaskClient,
        cliente_autenticado: dict[str, str | int],
        rota: str,
        titulo_esperado: str,
    ) -> None:
        """Todas as rotas de serviços financeiros devem renderizar seus respectivos formulários."""
        resposta = cliente.get(rota)
        assert resposta.status_code == 200
        assert titulo_esperado in resposta.get_data(as_text=True)

    def test_post_emprestimo_simulacao_aprovada(
        self, cliente: FlaskClient, cliente_autenticado: dict[str, str | int]
    ) -> None:
        """Simulação dentro dos limites deve exibir resultado aprovado com parcelamento."""
        dados = {
            "principal": "1000.00",
            "meses": "12",
            "renda": "6000.00",
            "sistema": "price",
        }
        resposta = cliente.post("/emprestimo", data=dados)
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "Resultado" in corpo
        assert "Aprovado." in corpo
        assert "1ª parcela: R$" in corpo
        assert "12 parcelas." in corpo

    def test_post_emprestimo_simulacao_recusada(
        self, cliente: FlaskClient, cliente_autenticado: dict[str, str | int]
    ) -> None:
        """Simulação com comprometimento acima da renda deve exibir resultado não aprovado."""
        dados = {
            "principal": "90000.00",
            "meses": "12",
            "renda": "1500.00",
            "sistema": "price",
        }
        resposta = cliente.post("/emprestimo", data=dados)
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "Resultado" in corpo
        assert "Não aprovado:" in corpo

    def test_post_tarifas_calculo_exibido(
        self, cliente: FlaskClient, cliente_autenticado: dict[str, str | int]
    ) -> None:
        """Consulta de tarifas deve calcular e exibir o valor da tarifa mensal."""
        dados = {
            "tipo": "corrente",
            "saldo": "2000.00",
            "transacoes": "5",
            "pacote": "on",
        }
        resposta = cliente.post("/tarifas", data=dados)
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "Tarifa mensal:" in corpo
        assert "R$ 30.00" in corpo

    def test_post_credito_analise_exibida(
        self, cliente: FlaskClient, cliente_autenticado: dict[str, str | int]
    ) -> None:
        """Análise de crédito deve retornar a situação, score calculado e limite sugerido."""
        dados = {
            "renda": "5000.00",
            "valor": "2000.00",
        }
        resposta = cliente.post("/credito", data=dados)
        assert resposta.status_code == 200
        corpo = resposta.get_data(as_text=True)
        assert "Resultado" in corpo
        assert "Situação:" in corpo
        assert "Score:" in corpo
        assert "Limite:" in corpo


class TestFluxoLogout:
    """Testa o encerramento de sessão via logout."""

    def test_logout_encerra_sessao_e_bloqueia_acessos_subsequentes(
        self, cliente: FlaskClient, cliente_autenticado: dict[str, str | int]
    ) -> None:
        """Após logout, a sessão deve ser limpa e novas tentativas de acesso devem ser redirecionadas."""
        # 1. Confirma que a sessão está autenticada
        resposta_inicial = cliente.get("/")
        assert resposta_inicial.status_code == 200

        # 2. Executa logout
        resposta_logout = cliente.get("/logout")
        assert resposta_logout.status_code == 302
        assert resposta_logout.headers["Location"] == "/login"

        # 3. Verifica que a chave cliente_id foi purgada da sessão
        with cliente.session_transaction() as sessao:
            assert "cliente_id" not in sessao

        # 4. Tenta acessar rota restrita e confirma novo bloqueio
        resposta_restrita = cliente.get("/", follow_redirects=False)
        assert resposta_restrita.status_code == 302
        assert resposta_restrita.headers["Location"] == "/login"
