from __future__ import annotations

from flask import Blueprint, render_template, session

from app.db import get_db
from app.repositorios.sqlite_repositorio import SqliteRepositorio
from app.web.helpers import login_required

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    repositorio = SqliteRepositorio(get_db)
    cliente = repositorio.buscar_cliente_por_id(session["cliente_id"])
    transacoes = repositorio.listar_transacoes(cliente.id)
    return render_template("dashboard.html", cliente=cliente, transacoes=transacoes)