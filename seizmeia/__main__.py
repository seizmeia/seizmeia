from __future__ import annotations

from pathlib import Path

import uvicorn  # type: ignore
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

from seizmeia.config import load_config_from_yaml
from seizmeia.health import router as health_router
from seizmeia.version import get_version

config = load_config_from_yaml(Path("seizmeia.yml"))

app = FastAPI()

# including healthcheck routes (/live and /ready)
app.include_router(health_router)


@app.get("/")
async def root() -> Response:
    return JSONResponse({"version": get_version()})


def run() -> None:
    uvicorn.run(
        "seizmeia.server:app",
        port=8000,
        host="0.0.0.0",
        loop="asyncio",
        reload=True,
        workers=1,
    )


if __name__ == "__main__":
    run()
