import pytest

from app.dominio.emprestimo import SimuladorEmprestimo, SistemaAmortizacao


@pytest.fixture
def simulador():
    return SimuladorEmprestimo()

class TestTaxaPorPrazo:
    """Testes aplicando Análise de Valor Limite e Partição de Equivalência"""
    
    @pytest.mark.parametrize("meses, taxa_esperada", [
        # Partição de Equivalência (classes válidas)
        (3, 0.025),   # <= 6
        (9, 0.03),    # 7 a 12
        (24, 0.035),  # 13 a 36
        (48, 0.04),   # > 36
        
        # Análise de Valor Limite
        (6, 0.025),   # Limite superior da 1ª classe
        (7, 0.03),    # Limite inferior da 2ª classe
        (12, 0.03),   # Limite superior da 2ª classe
        (13, 0.035),  # Limite inferior da 3ª classe
        (36, 0.035),  # Limite superior da 3ª classe
        (37, 0.04),   # Limite inferior da 4ª classe
    ])
    def test_taxa_por_prazo(self, simulador, meses, taxa_esperada):
        assert simulador.taxa_por_prazo(meses) == pytest.approx(taxa_esperada)

class TestTetoPorRenda:
    """Testes aplicando Análise de Valor Limite e Partição de Equivalência"""
    
    @pytest.mark.parametrize("renda, teto_esperado", [
        # Partição de Equivalência
        (-100.0, 0.0),        # Renda <= 0
        (1000.0, 150.0),      # Renda > 0 e < 2000 (15%)
        (3000.0, 600.0),      # Renda >= 2000 e < 5000 (20%)
        (7000.0, 1750.0),     # Renda >= 5000 e < 10000 (25%)
        (15000.0, 4500.0),    # Renda >= 10000 (30%)
        
        # Análise de Valor Limite
        (0.0, 0.0),           # Limite superior da 1ª classe
        (0.01, 0.0015),       # Limite inferior da 2ª classe
        (1999.99, 299.9985),  # Limite superior da 2ª classe
        (2000.0, 400.0),      # Limite inferior da 3ª classe
        (4999.99, 999.998),   # Limite superior da 3ª classe
        (5000.0, 1250.0),     # Limite inferior da 4ª classe
        (9999.99, 2499.9975), # Limite superior da 4ª classe
        (10000.0, 3000.0),    # Limite inferior da 5ª classe
    ])
    def test_teto_por_renda(self, simulador, renda, teto_esperado):
        assert simulador.teto_por_renda(renda) == pytest.approx(teto_esperado)

class TestParcelas:
    """Testes com foco nas lógicas de amortização e Teste de Laços (Loop Testing)"""

    def test_parcelas_price_taxa_zero(self, simulador):
        parcelas = simulador.parcelas_price(1000, 0.0, 10)
        assert len(parcelas) == 10
        assert parcelas == [100.0] * 10

    def test_parcelas_price_taxa_normal(self, simulador):
        parcelas = simulador.parcelas_price(1000, 0.03, 5)
        # Parcela = 1000 * 0.03 * (1.03^5) / ((1.03^5) - 1) = 218.3545... -> 218.35
        assert len(parcelas) == 5
        assert parcelas == [218.35] * 5

    # Teste de Laços para parcelas_sac (loop de 0 a 'meses'-1)
    
    def test_parcelas_sac_laco_zero(self, simulador):
        """Teste de loop: 0 iterações (pulando o laço inteiramente)"""
        with pytest.raises(ZeroDivisionError):
            simulador.parcelas_sac(1000, 0.03, 0)
        
    def test_parcelas_sac_laco_uma_iteracao(self, simulador):
        """Teste de loop: 1 iteração"""
        parcelas = simulador.parcelas_sac(1000, 0.03, 1)
        assert len(parcelas) == 1
        # Amortização: 1000. Juros: 1000*0.03 = 30. Total: 1030
        assert parcelas == [1030.0]

    def test_parcelas_sac_laco_n_iteracoes(self, simulador):
        """Teste de loop: n iterações (típico), avaliando o interior do laço multiplas vezes"""
        parcelas = simulador.parcelas_sac(1000, 0.03, 4)
        assert len(parcelas) == 4
        # Amortização = 250
        # Mês 1: Saldo 1000. Juros 30. Parcela 280
        # Mês 2: Saldo 750. Juros 22.5. Parcela 272.5
        # Mês 3: Saldo 500. Juros 15. Parcela 265
        # Mês 4: Saldo 250. Juros 7.5. Parcela 257.5
        assert parcelas == [280.0, 272.5, 265.0, 257.5]

class TestSimular:
    """Testes cobrindo validações (Partição de Equivalência), tetos e as vias de aprovação"""

    @pytest.mark.parametrize("principal, meses, renda, inadimplente, score, expected_motivo", [
        # Validações e Partições de Equivalência de Erro
        (0.0, 12, 5000.0, False, 500, "valor_invalido"),          # principal <= 0
        (99.99, 12, 5000.0, False, 500, "valor_abaixo_minimo"),   # principal < 100
        (1000.0, 1, 5000.0, False, 500, "prazo_curto"),           # meses < 2
        (1000.0, 61, 5000.0, False, 500, "prazo_longo"),          # meses > 60
        (1000.0, 12, 0.0, False, 500, "renda_invalida"),          # renda <= 0
        (1000.0, 12, -100.0, False, 500, "renda_invalida"),       # renda < 0
        (1000.0, 12, 5000.0, True, 500, "inadimplente"),          # inadimplente = True
        (1000.0, 12, 5000.0, False, 399, "score_baixo"),          # score < 400
    ])
    def test_simular_validacoes_iniciais(self, simulador, principal, meses, renda, inadimplente, score, expected_motivo):
        resultado = simulador.simular(principal, meses, renda, inadimplente=inadimplente, score=score)
        assert resultado.aprovado is False
        assert resultado.motivo == expected_motivo

    def test_simular_acima_teto(self, simulador):
        # Renda 3000 -> Teto de Empréstimo = 600 (3000 * 0.20)
        resultado = simulador.simular(principal=601.0, meses=12, renda=3000.0)
        assert resultado.aprovado is False
        assert resultado.motivo == "acima_teto"

    def test_simular_comprometimento_acima(self):
        # Precisamos de um teto_comprometimento baixo para forçar a rejeição
        simulador_estrito = SimuladorEmprestimo(teto_comprometimento=0.01) # 1% da renda
        # Renda 10000 -> Teto = 3000 (30%). Principal = 1000 (OK)
        # Parcela Price de 1000 em 10x ~ 100. 1% de 10000 = 100.
        # Parcela > 100 (juros vão tornar a parcela maior que 100)
        resultado = simulador_estrito.simular(principal=1000.0, meses=10, renda=10000.0)
        assert resultado.aprovado is False
        assert resultado.motivo == "comprometimento_acima"

    def test_simular_aprovado_price(self, simulador):
        resultado = simulador.simular(
            principal=1000.0, 
            meses=10, 
            renda=10000.0, 
            sistema=SistemaAmortizacao.PRICE
        )
        assert resultado.aprovado is True
        assert resultado.motivo == "aprovado"
        assert resultado.numero_parcelas == 10
        assert len(resultado.parcelas) == 10
        # taxa para 10 meses = 0.03 (base). Fator ~ 1.3439
        # Parcela ~ 117.23
        assert resultado.valor_parcela == 117.23
        assert resultado.total_pago == pytest.approx(117.23 * 10)

    def test_simular_aprovado_sac(self, simulador):
        resultado = simulador.simular(
            principal=1000.0, 
            meses=4, 
            renda=10000.0, 
            sistema=SistemaAmortizacao.SAC
        )
        assert resultado.aprovado is True
        assert resultado.motivo == "aprovado"
        assert resultado.numero_parcelas == 4
        # Taxa 4 meses = 0.025
        # Amortizacao = 250. Juros1 = 25. Parcela1 = 275.
        assert resultado.valor_parcela == 275.0
        assert len(resultado.parcelas) == 4
        assert resultado.parcelas == [275.0, 268.75, 262.5, 256.25]
        assert resultado.total_pago == sum([275.0, 268.75, 262.5, 256.25])

