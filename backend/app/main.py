"""FastAPI application entry point."""

from fastapi import FastAPI

from app.config import settings

app = FastAPI(
    title="WhatsApp AI Assistant API",
    version="0.1.0",
    debug=settings.app_debug,
)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Return the application health status."""

    return {"status": "ok"}
