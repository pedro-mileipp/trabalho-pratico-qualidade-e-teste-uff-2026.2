from __future__ import annotations

from flask import Blueprint, render_template, request

from app.dominio.emprestimo import ResultadoEmprestimo, SimuladorEmprestimo, SistemaAmortizacao
from app.web.helpers import login_required

bp = Blueprint("emprestimo", __name__)


@bp.route("/emprestimo", methods=["GET", "POST"])
@login_required
def simular():
    resultado = None
    if request.method == "POST":
        try:
            principal = float(request.form["principal"])
            meses = int(request.form["meses"])
            renda = float(request.form["renda"])
        except (TypeError, ValueError):
            resultado = ResultadoEmprestimo(False, "valor_invalido", 0, 0, 0, [])
        else:
            try:
                sistema = SistemaAmortizacao(request.form["sistema"])
            except (KeyError, ValueError):
                sistema = SistemaAmortizacao.PRICE
            resultado = SimuladorEmprestimo().simular(principal, meses, renda, sistema)
    return render_template("emprestimo.html", resultado=resultado)