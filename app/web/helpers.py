from __future__ import annotations

from functools import wraps

from flask import redirect, session, url_for


def login_required(rota):
    @wraps(rota)
    def envolvida(*args, **kwargs):
        if session.get("cliente_id") is None:
            return redirect(url_for("auth.login"))
        return rota(*args, **kwargs)

    return envolvida