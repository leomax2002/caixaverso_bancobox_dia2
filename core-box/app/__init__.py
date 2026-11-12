"""Core Box — Core Bancário do Banco Box (versão de laboratório).

ATENÇÃO: esta aplicação contém vulnerabilidades INTENCIONAIS para fins de
treinamento (Projeto Integrador DevSecOps — Dia 02). Não use em produção.
"""
import logging
import traceback

from flask import Flask, redirect, request, make_response
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import HTTPException

from app import config, db

csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(config.Config)
    if test_config:
        app.config.update(test_config)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    db.init_app(app)

    from app.auth import bp as auth_bp
    from app.contas import bp as contas_bp
    from app.pix import bp as pix_bp
    from app.backoffice import bp as backoffice_bp
    from app.onboarding import bp as onboarding_bp
    from app.api_interna import bp as interna_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(contas_bp)
    app.register_blueprint(pix_bp)
    app.register_blueprint(backoffice_bp)
    app.register_blueprint(onboarding_bp)
    app.register_blueprint(interna_bp)

    # Ativa proteção Anti-CSRF para os formulários web (/login, /abrir-conta, /recuperar)
    csrf.init_app(app)

    @app.before_request
    def isentar_csrf_para_apis():
        # Rotas de API REST autenticadas via JSON/JWT não dependem de cookie de sessão
        if request.path.startswith("/api/"):
            setattr(request, "csrf_valid", True)

    @app.after_request
    def aplicar_headers_seguranca(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "img-src 'self' data:; "
            "form-action 'self'; "
            "base-uri 'self'; "
            "frame-ancestors 'none';"
        )
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(self)"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        if not request.path.startswith("/static/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["Pragma"] = "no-cache"

        return response

    @app.route("/")
    def index():
        return redirect("/login")

    @app.route("/health")
    def health():
        return {"status": "ok", "app": "core-box"}

    @app.errorhandler(Exception)
    def erro_generico(exc):
        # Preserva códigos HTTP padrão (ex: 404 em /sitemap.xml e /robots.txt)
        if isinstance(exc, HTTPException):
            return make_response({"erro": exc.name}, exc.code)

        # Registra a stack trace apenas no log interno, sem expor ao cliente (CWE-209)
        detalhe = traceback.format_exc()
        app.logger.error("Erro não tratado: %s", detalhe)
        return make_response({"erro": "Erro interno do servidor."}, 500)

    return app
