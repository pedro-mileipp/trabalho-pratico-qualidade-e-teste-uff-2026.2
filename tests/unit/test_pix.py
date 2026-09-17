from datetime import time

import pytest

from app.dominio.pix import ChaveTipo, ConfiguracaoPix, ResultadoPix, TransacaoPix


@pytest.fixture
def pix():
    return TransacaoPix()


VALID_EMAIL = "user@example.com"
BLOQUEADAS = ["bloq@x.com"]


@pytest.mark.parametrize(
    ("chave", "tipo", "esperado"),
    [
        pytest.param("52998224725", ChaveTipo.CPF, True, id="cpf_valido"),
        pytest.param("11111111111", ChaveTipo.CPF, False, id="cpf_todos_digitos_iguais"),
        pytest.param("12345678901", ChaveTipo.CPF, False, id="cpf_dv_invalido"),
        pytest.param("123", ChaveTipo.CPF, False, id="cpf_poucos_digitos"),
        pytest.param("529982247250", ChaveTipo.CPF, False, id="cpf_digitos_demais"),
        pytest.param("abc", ChaveTipo.CPF, False, id="cpf_sem_digitos"),
        pytest.param("user@example.com", ChaveTipo.EMAIL, True, id="email_valido"),
        pytest.param("usuario.com", ChaveTipo.EMAIL, False, id="email_sem_arroba"),
        pytest.param("@example.com", ChaveTipo.EMAIL, False, id="email_local_vazio"),
        pytest.param(".user@example.com", ChaveTipo.EMAIL, False, id="email_local_ponto_inicio"),
        pytest.param("user.@example.com", ChaveTipo.EMAIL, False, id="email_local_ponto_fim"),
        pytest.param("user@example", ChaveTipo.EMAIL, False, id="email_dominio_sem_ponto"),
        pytest.param("user@.example.com", ChaveTipo.EMAIL, False, id="email_dominio_ponto_inicio"),
        pytest.param("user@example.com.", ChaveTipo.EMAIL, False, id="email_dominio_ponto_fim"),
        pytest.param("a@b@c.com", ChaveTipo.EMAIL, False, id="email_dois_arroba"),
        pytest.param("  user@example.com  ", ChaveTipo.EMAIL, True, id="email_com_espacos"),
        pytest.param(None, ChaveTipo.EMAIL, False, id="email_none"),
        pytest.param("2122223333", ChaveTipo.TELEFONE, True, id="telefone_10_digitos"),
        pytest.param("21988887777", ChaveTipo.TELEFONE, True, id="telefone_11_digitos"),
        pytest.param("212223333", ChaveTipo.TELEFONE, False, id="telefone_9_digitos"),
        pytest.param("212222333344", ChaveTipo.TELEFONE, False, id="telefone_12_digitos"),
        pytest.param("(21) 2222-3333", ChaveTipo.TELEFONE, True, id="telefone_formatado"),
        pytest.param("a" * 32, ChaveTipo.ALEATORIA, True, id="aleatoria_32_chars"),
        pytest.param("a" * 31, ChaveTipo.ALEATORIA, False, id="aleatoria_31_chars"),
        pytest.param("a" * 33, ChaveTipo.ALEATORIA, False, id="aleatoria_33_chars"),
        pytest.param("", ChaveTipo.EMAIL, False, id="chave_vazia"),
        pytest.param("x", None, False, id="tipo_invalido"),
    ],
)
def test_validar_chave(pix, chave, tipo, esperado):
    assert pix.validar_chave(chave, tipo) is esperado


@pytest.mark.parametrize(
    ("chave", "tipo", "valor", "saldo", "horario", "bloqueadas", "esperado"),
    [
        pytest.param("", ChaveTipo.EMAIL, 0, None, None, [], ResultadoPix.VALOR_INVALIDO, id="autorizar_valor_zero"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, -1, None, None, [], ResultadoPix.VALOR_INVALIDO, id="autorizar_valor_negativo"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, None, None, None, [], ResultadoPix.VALOR_INVALIDO, id="autorizar_valor_none"),
        pytest.param("chave@invalida", ChaveTipo.EMAIL, 100, 10000, time(12, 0), [], ResultadoPix.CHAVE_INVALIDA, id="autorizar_chave_invalida"),
        pytest.param("bloq@x.com", ChaveTipo.EMAIL, 100, 10000, time(12, 0), BLOQUEADAS, ResultadoPix.CHAVE_BLOQUEADA, id="autorizar_chave_bloqueada"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 5000.0, 10000, time(12, 0), [], ResultadoPix.APROVADA, id="autorizar_valor_limite_dia_exato"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 5000.01, 10000, time(12, 0), [], ResultadoPix.ACIMA_LIMITE, id="autorizar_acima_limite_dia"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 1000.0, 10000, time(21, 0), [], ResultadoPix.APROVADA, id="autorizar_valor_limite_noite_exato"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 1000.01, 10000, time(21, 0), [], ResultadoPix.FORA_HORARIO, id="autorizar_acima_limite_noite"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 2000, 100, time(21, 0), [], ResultadoPix.FORA_HORARIO, id="autorizar_limite_antes_saldo"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 100, 100, time(12, 0), [], ResultadoPix.APROVADA, id="autorizar_saldo_exato"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 100, 50, time(12, 0), [], ResultadoPix.SALDO_INSUFICIENTE, id="autorizar_saldo_insuficiente"),
        pytest.param(VALID_EMAIL, ChaveTipo.EMAIL, 100, 10000, time(12, 0), [], ResultadoPix.APROVADA, id="autorizar_sucesso"),
    ],
)
def test_autorizar(chave, tipo, valor, saldo, horario, bloqueadas, esperado):
    pix = TransacaoPix(ConfiguracaoPix(chaves_bloqueadas=bloqueadas))
    assert pix.autorizar(chave, tipo, valor, saldo, horario) is esperado


@pytest.mark.parametrize(
    ("chave", "valor", "dias", "motivo", "bloqueadas", "esperado"),
    [
        pytest.param(VALID_EMAIL, 100, -1, None, [], False, id="chargeback_dias_negativo"),
        pytest.param(VALID_EMAIL, 100, 91, None, [], False, id="chargeback_dias_91"),
        pytest.param(VALID_EMAIL, 100, 90, None, [], False, id="chargeback_dias_90"),
        pytest.param(VALID_EMAIL, 0, 30, None, [], False, id="chargeback_valor_zero"),
        pytest.param(VALID_EMAIL, -5, 30, None, [], False, id="chargeback_valor_negativo"),
        pytest.param("bloq@x.com", 999999, 30, None, BLOQUEADAS, False, id="chargeback_bloqueada_dias_30_valor_alto"),
        pytest.param(VALID_EMAIL, 100, 60, "golpe", [], True, id="chargeback_motivo_golpe"),
        pytest.param(VALID_EMAIL, 100, 60, "FRAUDE", [], True, id="chargeback_motivo_fraude_maiusculo"),
        pytest.param(VALID_EMAIL, 100, 60, "", [], False, id="chargeback_motivo_vazio"),
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
    ],
)
def test_eh_noturno(inicio, fim, momento, esperado):
    pix = TransacaoPix(
        ConfiguracaoPix(inicio_noturno=inicio, fim_noturno=fim)
    )
    assert pix._eh_noturno(momento) is esperado