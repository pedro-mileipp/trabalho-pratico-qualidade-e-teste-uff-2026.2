from __future__ import annotations

from flask import Blueprint, render_template, request

from app.dominio.credito import DecisorCredito, ResultadoCredito, SituacaoCredito
from app.web.helpers import login_required

bp = Blueprint("credito", __name__)


@bp.route("/credito", methods=["GET", "POST"])
@login_required
def consultar():
    resultado = None
    if request.method == "POST":
        try:
            renda = float(request.form["renda"])
            valor = float(request.form["valor"])
        except (TypeError, ValueError):
            resultado = ResultadoCredito(SituacaoCredito.NEGADO, 0, 0, "valor_invalido")
        else:
            resultado = DecisorCredito().decidir([], renda, valor)
    return render_template("credito.html", resultado=resultado)