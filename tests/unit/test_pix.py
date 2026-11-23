"""Testes unitários de `TransacaoPix` (issue #3; ampliados na #38).

Organização por técnica — o id do ``pytest.param`` identifica a técnica:

- ``pe_``: partição de equivalência
- ``vl_``: análise de valor-limite
- ``td_``: tabela de decisão
- ``laco_``: teste de laços
- ``custom_``: parâmetros customizados via `ConfiguracaoPix`

Os casos da Entrega 1 mantêm os ids originais (sem prefixo) para preservar as
referências das issues #16 e #17 (regressões identificadas em comentário).
"""

from datetime import time

import pytest

from app.dominio.pix import ChaveTipo, ConfiguracaoPix, ResultadoPix, TransacaoPix


@pytest.fixture
def pix():
    return TransacaoPix()


VALID_EMAIL = "user@example.com"
BLOQUEADAS = ["bloq@x.com"]


# ---------------------------------------------------------------------------
# validar_chave — partição de equivalência, valor-limite e laço (CPF)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("chave", "tipo", "esperado"),
    [
        # --- CPF (algoritmo dos dois dígitos verificadores) ---
        pytest.param("52998224725", ChaveTipo.CPF, True, id="cpf_valido"),
        pytest.param("529.982.247-25", ChaveTipo.CPF, True, id="pe_cpf_valido_formatado"),
        pytest.param("5299822472a", ChaveTipo.CPF, False, id="pe_cpf_com_letras"),
        pytest.param("11111111111", ChaveTipo.CPF, False, id="cpf_todos_digitos_iguais"),
        pytest.param("12345678901", ChaveTipo.CPF, False, id="cpf_dv_invalido"),
        pytest.param("52998224735", ChaveTipo.CPF, False, id="laco_cpf_falha_primeiro_dv"),
        pytest.param("52998224726", ChaveTipo.CPF, False, id="laco_cpf_falha_segundo_dv"),
        pytest.param("123", ChaveTipo.CPF, False, id="cpf_poucos_digitos"),
        pytest.param("529982247250", ChaveTipo.CPF, False, id="cpf_digitos_demais"),
        pytest.param("abc", ChaveTipo.CPF, False, id="cpf_sem_digitos"),
        # --- e-mail ---
        pytest.param("user@example.com", ChaveTipo.EMAIL, True, id="email_valido"),
        pytest.param("usuario.com", ChaveTipo.EMAIL, False, id="email_sem_arroba"),
        pytest.param("@example.com", ChaveTipo.EMAIL, False, id="email_local_vazio"),
        pytest.param(".user@example.com", ChaveTipo.EMAIL, False, id="email_local_ponto_inicio"),
        pytest.param("user.@example.com", ChaveTipo.EMAIL, False, id="email_local_ponto_fim"),
        pytest.param("user@example", ChaveTipo.EMAIL, False, id="email_dominio_sem_ponto"),
        pytest.param("user@.example.com", ChaveTipo.EMAIL, False, id="email_dominio_ponto_inicio"),
        pytest.param("user@example.com.", ChaveTipo.EMAIL, False, id="email_dominio_ponto_fim"),
        # regressão do defeito #16 (corrigido no commit e7881bd)
        pytest.param("a@b@c.com", ChaveTipo.EMAIL, False, id="email_dois_arroba"),
        pytest.param("a@b@c@d.com", ChaveTipo.EMAIL, False, id="pe_email_tres_arrobas"),
        pytest.param("  user@example.com  ", ChaveTipo.EMAIL, True, id="email_com_espacos"),
        pytest.param(None, ChaveTipo.EMAIL, False, id="email_none"),
        # --- telefone ---
        pytest.param("2122223333", ChaveTipo.TELEFONE, True, id="telefone_10_digitos"),
        pytest.param("21988887777", ChaveTipo.TELEFONE, True, id="telefone_11_digitos"),
        pytest.param("212223333", ChaveTipo.TELEFONE, False, id="telefone_9_digitos"),
        pytest.param("212222333344", ChaveTipo.TELEFONE, False, id="telefone_12_digitos"),
        pytest.param("(21) 2222-3333", ChaveTipo.TELEFONE, True, id="telefone_formatado"),
        # --- aleatória ---
        pytest.param("a" * 32, ChaveTipo.ALEATORIA, True, id="aleatoria_32_chars"),
        pytest.param("a" * 31, ChaveTipo.ALEATORIA, False, id="aleatoria_31_chars"),
        pytest.param("a" * 33, ChaveTipo.ALEATORIA, False, id="aleatoria_33_chars"),
        pytest.param("  " + "a" * 32 + "  ", ChaveTipo.ALEATORIA, True, id="pe_aleatoria_com_espacos"),
        # --- vazio e tipo desconhecido ---
        pytest.param("", ChaveTipo.EMAIL, False, id="chave_vazia"),
        pytest.param("x", None, False, id="tipo_invalido"),
    ],
)
def test_validar_chave(pix, chave, tipo, esperado):
    assert pix.validar_chave(chave, tipo) is esperado


# ---------------------------------------------------------------------------
# autorizar — tabela de decisão e análise de valor-limite
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("chave", "tipo", "valor", "saldo", "horario", "bloqueadas", "esperado"),
    [
        # --- valor inválido (precedência 1) ---
        pytest.param("", ChaveTipo.EMAIL, 0, None, None, [], ResultadoPix.VALOR_INVALIDO, id="autorizar_valor_zero"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, -1, None, None, [], ResultadoPix.VALOR_INVALIDO, id="autorizar_valor_negativo"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, None, None, None, [], ResultadoPix.VALOR_INVALIDO, id="autorizar_valor_none"),
        # --- chave inválida (precedência 2) ---
        pytest.param("chave@invalida", ChaveTipo.EMAIL, 100, 10000, time(12, 0), [], ResultadoPix.CHAVE_INVALIDA, id="autorizar_chave_invalida"),
        # --- chave bloqueada (precedência 3) ---
        pytest.param("bloq@x.com", ChaveTipo.EMAIL, 100, 10000, time(12, 0), BLOQUEADAS, ResultadoPix.CHAVE_BLOQUEADA, id="autorizar_chave_bloqueada"),
        # --- precedências da tabela de decisão ---
        pytest.param("bloq@x.com", ChaveTipo.EMAIL, 0, 10000, time(12, 0), BLOQUEADAS, ResultadoPix.VALOR_INVALIDO, id="td_bloqueada_com_valor_zero"),
        pytest.param("chave@invalida", ChaveTipo.EMAIL, 100, 10000, time(12, 0), BLOQUEADAS, ResultadoPix.CHAVE_INVALIDA, id="td_chave_invalida_mesmo_bloqueada"),
        # --- limite diurno (valor-limite) ---
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 5000.0, 10000, time(12, 0), [], ResultadoPix.APROVADA, id="autorizar_valor_limite_dia_exato"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 5000.01, 10000, time(12, 0), [], ResultadoPix.ACIMA_LIMITE, id="autorizar_acima_limite_dia"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 4999.99, 10000, time(12, 0), [], ResultadoPix.APROVADA, id="vl_dia_abaixo_do_limite"),
        # --- limite noturno (valor-limite) ---
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 1000.0, 10000, time(21, 0), [], ResultadoPix.APROVADA, id="autorizar_valor_limite_noite_exato"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 1000.01, 10000, time(21, 0), [], ResultadoPix.FORA_HORARIO, id="autorizar_acima_limite_noite"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 999.99, 10000, time(21, 0), [], ResultadoPix.APROVADA, id="vl_noite_abaixo_do_limite"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 2000, 100, time(21, 0), [], ResultadoPix.FORA_HORARIO, id="autorizar_limite_antes_saldo"),
        # --- fronteiras do horário (janela 20h–6h) ---
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 5000.01, 10000, time(19, 59), [], ResultadoPix.ACIMA_LIMITE, id="vl_19h59_diurno"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 1000.01, 10000, time(20, 0), [], ResultadoPix.FORA_HORARIO, id="vl_20h00_noturno"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 1000.01, 10000, time(5, 59), [], ResultadoPix.FORA_HORARIO, id="vl_5h59_noturno"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 1000.01, 10000, time(6, 0), [], ResultadoPix.FORA_HORARIO, id="vl_6h00_noturno"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 5000.01, 10000, time(6, 1), [], ResultadoPix.ACIMA_LIMITE, id="vl_6h01_diurno"),
        # --- saldo (valor-limite e ausência de saldo) ---
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 100, 100, time(12, 0), [], ResultadoPix.APROVADA, id="autorizar_saldo_exato"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 100, 99.99, time(12, 0), [], ResultadoPix.SALDO_INSUFICIENTE, id="vl_saldo_abaixo_um_centavo"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 100, 100.01, time(12, 0), [], ResultadoPix.APROVADA, id="vl_saldo_acima_um_centavo"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 100, 50, time(12, 0), [], ResultadoPix.SALDO_INSUFICIENTE, id="autorizar_saldo_insuficiente"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 100, None, time(12, 0), [], ResultadoPix.APROVADA, id="pe_sem_saldo_aprova"),
        # --- sucesso ---
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 100, 10000, time(12, 0), [], ResultadoPix.APROVADA, id="autorizar_sucesso"),
    ],
)
def test_autorizar(chave, tipo, valor, saldo, horario, bloqueadas, esperado):
    pix = TransacaoPix(ConfiguracaoPix(chaves_bloqueadas=bloqueadas))
    assert pix.autorizar(chave, tipo, valor, saldo, horario) is esperado


# ---------------------------------------------------------------------------
# autorizar — parâmetros customizados (limites próprios)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("valor", "saldo", "horario", "esperado"),
    [
        pytest.param(100.0, 1000, time(12, 0), ResultadoPix.APROVADA, id="custom_dia_no_teto"),
        pytest.param(100.01, 1000, time(12, 0), ResultadoPix.ACIMA_LIMITE, id="custom_dia_acima_do_teto"),
        pytest.param(50.0, 1000, time(21, 0), ResultadoPix.APROVADA, id="custom_noite_no_teto"),
        pytest.param(50.01, 1000, time(21, 0), ResultadoPix.FORA_HORARIO, id="custom_noite_acima_do_teto"),
    ],
)
def test_autorizar_configuracao_customizada(valor, saldo, horario, esperado):
    pix = TransacaoPix(ConfiguracaoPix(limite_padrao=100.0, limite_noturno=50.0))
    assert pix.autorizar(VALID_EMAIL, ChaveTipo.EMAIL, valor, saldo, horario) is esperado


# ---------------------------------------------------------------------------
# solicitar_chargeback — tabela de decisão
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("chave", "valor", "dias", "motivo", "bloqueadas", "esperado"),
    [
        pytest.param(VALID_EMAIL, 100, -1, None, [], False, id="chargeback_dias_negativo"),
        pytest.param(VALID_EMAIL, 100, 91, None, [], False, id="chargeback_dias_91"),
        pytest.param(VALID_EMAIL, 100, 90, None, [], False, id="chargeback_dias_90"),
        pytest.param(VALID_EMAIL, 0, 30, None, [], False, id="chargeback_valor_zero"),
        pytest.param(VALID_EMAIL, -5, 30, None, [], False, id="chargeback_valor_negativo"),
        # regressão do defeito #17 (corrigido no commit e7881bd)
        pytest.param("bloq@x.com", 999999, 30, None, BLOQUEADAS, False, id="chargeback_bloqueada_dias_30_valor_alto"),
        # --- chave bloqueada nas demais faixas da tabela de decisão ---
        pytest.param("bloq@x.com", 100, 7, None, BLOQUEADAS, False, id="td_bloqueada_dias_7"),
        pytest.param("bloq@x.com", 100, 60, "golpe", BLOQUEADAS, False, id="td_bloqueada_com_motivo_golpe"),
        pytest.param("bloq@x.com", 0, 30, None, BLOQUEADAS, False, id="td_bloqueada_valor_zero"),
        # --- motivo ---
        pytest.param(VALID_EMAIL, 100, 60, "golpe", [], True, id="chargeback_motivo_golpe"),
        pytest.param(VALID_EMAIL, 100, 60, "FRAUDE", [], True, id="chargeback_motivo_fraude_maiusculo"),
        pytest.param(VALID_EMAIL, 100, 60, "", [], False, id="chargeback_motivo_vazio"),
        pytest.param(VALID_EMAIL, 100, 90, "golpe", [], True, id="td_golpe_no_ultimo_dia"),
        pytest.param(VALID_EMAIL, 100, 91, "golpe", [], False, id="td_golpe_acima_do_prazo"),
        pytest.param(VALID_EMAIL, 5000, 30, "fraude", [], True, id="td_fraude_ignora_valor"),
        # --- prazo e valor (valor-limite) ---
        pytest.param(VALID_EMAIL, 100, 0, None, [], True, id="chargeback_dias_zero"),
        pytest.param(VALID_EMAIL, 100, 7, None, [], True, id="chargeback_dias_7"),
        pytest.param(VALID_EMAIL, 100, 8, None, [], True, id="chargeback_dias_8_valor_baixo"),
        pytest.param(VALID_EMAIL, 6000, 8, None, [], False, id="chargeback_dias_8_valor_alto"),
        pytest.param(VALID_EMAIL, 5000, 30, None, [], True, id="chargeback_dias_30_valor_exato"),
        pytest.param(VALID_EMAIL, 5000.01, 30, None, [], False, id="chargeback_dias_30_valor_alto"),
        pytest.param(VALID_EMAIL, 100, 31, None, [], False, id="chargeback_dias_31"),
    ],
)
def test_solicitar_chargeback(chave, valor, dias, motivo, bloqueadas, esperado):
    pix = TransacaoPix(ConfiguracaoPix(chaves_bloqueadas=bloqueadas))
    assert pix.solicitar_chargeback(chave, valor, dias, motivo) is esperado


# ---------------------------------------------------------------------------
# solicitar_chargeback — parâmetros customizados (prazo próprio)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("dias", "valor", "esperado"),
    [
        pytest.param(15, 100.0, True, id="custom_chargeback_no_teto_dos_dias"),
        pytest.param(16, 100.0, False, id="custom_chargeback_acima_dos_dias"),
        pytest.param(8, 100.01, False, id="custom_chargeback_acima_do_valor"),
        pytest.param(8, 100.0, True, id="custom_chargeback_no_teto_do_valor"),
    ],
)
def test_chargeback_configuracao_customizada(dias, valor, esperado):
    pix = TransacaoPix(ConfiguracaoPix(limite_padrao=100.0, limite_chargeback_dias=15))
    assert pix.solicitar_chargeback(VALID_EMAIL, valor, dias) is esperado


# ---------------------------------------------------------------------------
# _eh_noturno — partição de equivalência e valor-limite
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("inicio", "fim", "momento", "esperado"),
    [
        pytest.param(time(20, 0), time(6, 0), time(21, 0), True, id="noturno_21h"),
        pytest.param(time(20, 0), time(6, 0), time(5, 0), True, id="noturno_5h"),
        pytest.param(time(20, 0), time(6, 0), time(20, 0), True, id="noturno_20h_exato"),
        pytest.param(time(20, 0), time(6, 0), time(6, 0), True, id="noturno_6h_exato"),
        pytest.param(time(20, 0), time(6, 0), time(6, 1), False, id="noturno_6h1min"),
        pytest.param(time(20, 0), time(6, 0), time(19, 59), False, id="noturno_19h59"),
        pytest.param(time(20, 0), time(6, 0), time(12, 0), False, id="noturno_12h"),
        pytest.param(time(8, 0), time(18, 0), time(10, 0), True, id="noturno_custom_10h"),
        pytest.param(time(8, 0), time(18, 0), time(8, 0), True, id="noturno_custom_8h_exato"),
        pytest.param(time(8, 0), time(18, 0), time(18, 0), True, id="noturno_custom_18h_exato"),
        pytest.param(time(8, 0), time(18, 0), time(19, 0), False, id="noturno_custom_19h"),
        pytest.param(time(8, 0), time(18, 0), time(7, 59), False, id="noturno_custom_7h59"),
        pytest.param(time(22, 0), time(2, 0), time(23, 0), True, id="noturno_custom_virada_23h"),
        pytest.param(time(22, 0), time(2, 0), time(1, 0), True, id="noturno_custom_virada_1h"),
        pytest.param(time(22, 0), time(2, 0), time(21, 59), False, id="noturno_custom_virada_antes"),
        pytest.param(time(22, 0), time(2, 0), time(2, 1), False, id="noturno_custom_virada_depois"),
    ],
)
def test_eh_noturno(inicio, fim, momento, esperado):
    pix = TransacaoPix(
        ConfiguracaoPix(inicio_noturno=inicio, fim_noturno=fim)
    )
    assert pix._eh_noturno(momento) is esperado
