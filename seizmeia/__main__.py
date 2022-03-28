from __future__ import annotations

from pathlib import Path

import uvicorn  # type: ignore
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse, Response

from seizmeia.db import Base, engine
from seizmeia.health import router as health_router
from seizmeia.settings import Settings
from seizmeia.user.auth.token import router as token_router
from seizmeia.user.routes import router as user_router
from seizmeia.version import get_version

config = Settings()

app = FastAPI(
    title="Seizmeia 🍺",
    description="A credit management tool for a beer tap.",
    version=get_version(),
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(health_router)
app.include_router(token_router)


@app.get("/")
async def root() -> Response:
    return JSONResponse({"version": get_version()})


def run() -> None:
    uvicorn.run(
        "seizmeia.__main__:app",
        port=8000,
        host="0.0.0.0",
        loop="asyncio",
        reload=True,
        workers=1,
    )


if __name__ == "__main__":
    run()
