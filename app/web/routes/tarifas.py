from __future__ import annotations

from flask import Blueprint, render_template, request

from app.dominio.tarifas import TarifaBancaria, TarifasBase, TipoConta
from app.web.helpers import login_required

bp = Blueprint("tarifas", __name__)


@bp.route("/tarifas", methods=["GET", "POST"])
@login_required
def consultar():
    tarifa = None
    if request.method == "POST":
        try:
            tipo = TipoConta(request.form["tipo"])
        except (KeyError, ValueError):
            tipo = TipoConta.CORRENTE
        try:
            saldo = float(request.form["saldo"])
        except (TypeError, ValueError):
            saldo = 0.0
        try:
            transacoes = int(request.form["transacoes"])
        except (TypeError, ValueError):
            transacoes = 0
        pacote = request.form.get("pacote") == "on"
        tarifa = TarifaBancaria(TarifasBase()).tarifa_mensal(tipo, saldo, pacote, transacoes)
    return render_template("tarifas.html", tarifa=tarifa)