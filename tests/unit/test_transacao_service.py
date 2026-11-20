from __future__ import annotations

from datetime import time

import pytest

from app.dominio.pix import ChaveTipo, ResultadoPix, TransacaoPix
from app.modelos import Cliente
from app.repositorios.repositorio import Repositorio
from app.servicos.transacoes import TransacaoRecusada, TransacaoService


@pytest.fixture
def repositorio_mock(mocker):
    return mocker.Mock(spec=Repositorio)


@pytest.fixture
def servico(repositorio_mock) -> TransacaoService:
    return TransacaoService(repositorio=repositorio_mock)


class TestTransferirPix:
    def test_cliente_inexistente_levanta_transacao_recusada_sem_persistir(
        self, servico: TransacaoService, repositorio_mock
    ) -> None:
        repositorio_mock.buscar_cliente_por_id.return_value = None

        with pytest.raises(TransacaoRecusada) as exc_info:
            servico.transferir_pix(
                cliente_id=999,
                chave="maria@exemplo.com",
                tipo=ChaveTipo.EMAIL,
                valor=100.0,
            )

        assert exc_info.value.resultado is ResultadoPix.CHAVE_INVALIDA
        repositorio_mock.buscar_cliente_por_id.assert_called_once_with(999)
        repositorio_mock.atualizar_saldo.assert_not_called()
        repositorio_mock.registrar_transacao.assert_not_called()

    def test_pix_recusado_nao_chama_atualizar_saldo_nem_registrar_transacao(
        self, servico: TransacaoService, repositorio_mock
    ) -> None:
        repositorio_mock.buscar_cliente_por_id.return_value = Cliente(
            id=1,
            nome="Maria",
            email="maria@exemplo.com",
            senha_hash="hash_fake",
            saldo=50.0,
        )

        with pytest.raises(TransacaoRecusada) as exc_info:
            servico.transferir_pix(
                cliente_id=1,
                chave="maria@exemplo.com",
                tipo=ChaveTipo.EMAIL,
                valor=200.0,
            )

        assert exc_info.value.resultado is not ResultadoPix.APROVADA
        repositorio_mock.atualizar_saldo.assert_not_called()
        repositorio_mock.registrar_transacao.assert_not_called()

    def test_pix_aprovado_retorna_novo_saldo_e_chama_repositorio_com_argumentos_corretos(
        self, servico: TransacaoService, repositorio_mock
    ) -> None:
        repositorio_mock.buscar_cliente_por_id.return_value = Cliente(
            id=1,
            nome="Maria",
            email="maria@exemplo.com",
            senha_hash="hash_fake",
            saldo=500.0,
        )
        horario = time(12, 0, 0)

        novo_saldo = servico.transferir_pix(
            cliente_id=1,
            chave="maria@exemplo.com",
            tipo=ChaveTipo.EMAIL,
            valor=125.50,
            horario=horario,
        )

        assert novo_saldo == pytest.approx(374.50)
        repositorio_mock.atualizar_saldo.assert_called_once_with(1, 374.50)
        repositorio_mock.registrar_transacao.assert_called_once_with(
            1,
            "pix",
            f"PIX {ChaveTipo.EMAIL.value}",
            -125.50,
        )

    def test_pix_aprovado_com_transacao_pix_mockado(
        self, repositorio_mock, mocker
    ) -> None:
        repositorio_mock.buscar_cliente_por_id.return_value = Cliente(
            id=2,
            nome="João",
            email="joao@exemplo.com",
            senha_hash="hash_fake",
            saldo=1000.0,
        )
        pix_mock = mocker.Mock(spec=TransacaoPix)
        pix_mock.autorizar.return_value = ResultadoPix.APROVADA
        mocker.patch(
            "app.servicos.transacoes.TransacaoPix",
            return_value=pix_mock,
        )

        servico_mockado = TransacaoService(repositorio=repositorio_mock)
        horario = time(14, 30, 0)

        novo_saldo = servico_mockado.transferir_pix(
            cliente_id=2,
            chave="12345678901",
            tipo=ChaveTipo.CPF,
            valor=300.0,
            horario=horario,
        )

        pix_mock.autorizar.assert_called_once_with(
            "12345678901",
            ChaveTipo.CPF,
            300.0,
            1000.0,
            horario,
        )
        assert novo_saldo == 700.0
        repositorio_mock.atualizar_saldo.assert_called_once_with(2, 700.0)
        repositorio_mock.registrar_transacao.assert_called_once_with(
            2,
            "pix",
            f"PIX {ChaveTipo.CPF.value}",
            -300.0,
        )