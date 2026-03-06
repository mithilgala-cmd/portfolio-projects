"""
config.py — Loads configuration from config.yml and .env.
"""

import logging
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"
CONFIG_FILE = BASE_DIR / "config.yml"

# ── Load .env ──────────────────────────────────────────────────────────
load_dotenv(dotenv_path=ENV_FILE)


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)


# ── Load YAML config ───────────────────────────────────────────────────
_cfg = _load_yaml(CONFIG_FILE)

# ── App settings ───────────────────────────────────────────────────────
APP_NAME: str = _cfg["app"]["name"]
APP_VERSION: str = _cfg["app"]["version"]
APP_DESCRIPTION: str = _cfg["app"]["description"]

# ── Server settings ────────────────────────────────────────────────────
SERVER_HOST: str = _cfg["server"]["host"]
SERVER_PORT: int = _cfg["server"]["port"]

# ── NewsAPI settings ───────────────────────────────────────────────────
NEWSAPI_BASE_URL: str = _cfg["newsapi"]["base_url"]
NEWSAPI_KEY: str = os.getenv("NEWS_API_KEY", "")
DEFAULT_COUNTRY: str = _cfg["newsapi"]["default_country"]
DEFAULT_LANGUAGE: str = _cfg["newsapi"]["default_language"]
DEFAULT_PAGE_SIZE: int = _cfg["newsapi"]["default_page_size"]
MAX_PAGE_SIZE: int = _cfg["newsapi"]["max_page_size"]

# ── Cache settings ─────────────────────────────────────────────────────
CACHE_TTL_SECONDS: int = _cfg["cache"]["ttl_seconds"]

# ── Logging ────────────────────────────────────────────────────────────
LOG_LEVEL: str = _cfg["logging"]["level"]
LOG_FORMAT: str = _cfg["logging"]["format"]

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

if not NEWSAPI_KEY:
    logger.warning(
        "NEWS_API_KEY is not set. "
        "Copy .env.example to .env and add your key from https://newsapi.org/register"
    )
