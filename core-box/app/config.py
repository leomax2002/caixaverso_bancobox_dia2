"""Configuração do Core Box.

Decisão do time (Dia 01, premissa P-03): "o .env saiu do Git, então está tudo certo".
"""
import os

import yaml

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def _carregar_yaml(caminho):
    with open(caminho, encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


_cfg = _carregar_yaml(os.path.join(BASE_DIR, "config", "app-config.yaml"))


class Config:
    VERSAO = _cfg["app"]["versao"]
    AMBIENTE = os.getenv("BOX_AMBIENTE", _cfg["app"]["ambiente"])
    DEBUG = False
    DATABASE = os.getenv("BOX_DATABASE", os.path.join(BASE_DIR, "box.db"))
    UPLOAD_DIR = os.getenv("BOX_UPLOAD_DIR", os.path.join(BASE_DIR, "uploads"))

    # Segredos carregados via variáveis de ambiente
    SECRET_KEY = os.getenv("BOX_SECRET_KEY") or "fallback-apenas-para-testes-locais"
    JWT_SECRET = os.getenv("BOX_JWT_SECRET")
    JWT_EXPIRACAO_HORAS = 24 * 7

    # Controle do CSRF (ativo em homolog/prod, desativável nos testes via env ou test_config)
    WTF_CSRF_ENABLED = os.getenv("WTF_CSRF_ENABLED", "true").lower() == "true"

    PSTI_URL = _cfg["integracoes"]["psti_url"]
    PSTI_API_KEY = os.getenv("BOX_PSTI_API_KEY")
    SMS_GATEWAY_TOKEN = os.getenv("BOX_SMS_GATEWAY_TOKEN")

    LIMITE_DIURNO_PADRAO = _cfg["pix"]["limite_diurno"]
    LIMITE_NOTURNO_PADRAO = _cfg["pix"]["limite_noturno"]
    ANTIFRAUDE_TIMEOUT_S = _cfg["antifraude"]["timeout_segundos"]
