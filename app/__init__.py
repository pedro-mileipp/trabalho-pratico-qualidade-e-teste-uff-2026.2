from __future__ import annotations

from flask import Flask

from .config import Config
from .db import init_db


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_db(app)

    from .web.routes.auth import bp as auth_bp
    from .web.routes.credito import bp as credito_bp
    from .web.routes.dashboard import bp as dashboard_bp
    from .web.routes.emprestimo import bp as emprestimo_bp
    from .web.routes.pix import bp as pix_bp
    from .web.routes.tarifas import bp as tarifas_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pix_bp)
    app.register_blueprint(emprestimo_bp)
    app.register_blueprint(tarifas_bp)
    app.register_blueprint(credito_bp)

    return app