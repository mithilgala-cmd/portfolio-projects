"""
main.py — FastAPI application entry point.

Registers routers, configures CORS, and manages the httpx client lifecycle.
"""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import config, fetcher
from src.routers import health, news

logger = logging.getLogger(__name__)


# ── Lifespan: open/close shared HTTP client ────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    fetcher.get_client()          # warm up client on startup
    yield
    await fetcher.close_client()  # clean up on shutdown
    logger.info("Server shut down cleanly.")


# ── App ────────────────────────────────────────────────────────────────
app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description=config.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(news.router)


# ── Root redirect info ─────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": f"Welcome to {config.APP_NAME}",
        "version": config.APP_VERSION,
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "top_headlines": "/news/top-headlines",
            "search": "/news/search",
            "sources": "/news/sources",
        },
    }


# ── Dev runner ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=True,
    )
