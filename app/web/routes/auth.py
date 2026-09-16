from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.db import get_db
from app.repositorios.sqlite_repositorio import SqliteRepositorio
from app.servicos.auth import AuthService, CredenciaisInvalidas, EmailJaCadastrado

bp = Blueprint("auth", __name__)


def _repositorio() -> SqliteRepositorio:
    return SqliteRepositorio(get_db)


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        try:
            cliente = AuthService(_repositorio()).registrar(
                request.form["nome"],
                request.form["email"],
                request.form["senha"],
            )
        except EmailJaCadastrado:
            flash("Este e-mail já está cadastrado.", "erro")
            return render_template("registro.html")
        except CredenciaisInvalidas:
            flash("Dados inválidos. Verifique os campos.", "erro")
            return render_template("registro.html")
        session["cliente_id"] = cliente.id
        return redirect(url_for("dashboard.index"))
    return render_template("registro.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            cliente = AuthService(_repositorio()).autenticar(
                request.form["email"],
                request.form["senha"],
            )
        except CredenciaisInvalidas:
            flash("E-mail ou senha inválidos.", "erro")
            return render_template("login.html")
        session["cliente_id"] = cliente.id
        return redirect(url_for("dashboard.index"))
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))