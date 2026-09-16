from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.db import get_db
from app.dominio.pix import ChaveTipo, ResultadoPix
from app.repositorios.sqlite_repositorio import SqliteRepositorio
from app.servicos.transacoes import TransacaoRecusada, TransacaoService
from app.web.helpers import login_required

bp = Blueprint("pix", __name__)

_MENSAGENS = {
    ResultadoPix.CHAVE_INVALIDA: "Chave PIX inválida.",
    ResultadoPix.VALOR_INVALIDO: "Valor inválido.",
    ResultadoPix.CHAVE_BLOQUEADA: "Chave bloqueada.",
    ResultadoPix.ACIMA_LIMITE: "Valor acima do limite permitido.",
    ResultadoPix.FORA_HORARIO: "Operação fora do horário permitido.",
    ResultadoPix.SALDO_INSUFICIENTE: "Saldo insuficiente.",
}


@bp.route("/pix", methods=["GET", "POST"])
@login_required
def transferir():
    if request.method == "POST":
        try:
            valor = float(request.form["valor"])
        except (TypeError, ValueError):
            flash("Valor inválido.", "erro")
            return render_template("pix.html")
        try:
            tipo = ChaveTipo(request.form["tipo"])
        except (KeyError, ValueError):
            tipo = ChaveTipo.CPF
        try:
            TransacaoService(SqliteRepositorio(get_db)).transferir_pix(
                session["cliente_id"],
                request.form["chave"],
                tipo,
                valor,
            )
        except TransacaoRecusada as exc:
            flash(_MENSAGENS.get(exc.resultado, "Transferência recusada."), "erro")
            return render_template("pix.html")
        flash("Transferência realizada com sucesso.", "sucesso")
        return redirect(url_for("dashboard.index"))
    return render_template("pix.html")