from __future__ import annotations
from sys import prefix

import uvicorn  # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from seizmeia.db import Base, engine
from seizmeia.health import router as health_router
from seizmeia.settings import Settings
from seizmeia.token.route import router as token_router
from seizmeia.user.routes import router as user_router
from seizmeia.version import router as version_router, get_version

config = Settings()

app = FastAPI(
    title="Seizmeia 🍺",
    description="A credit management tool for a beer tap.",
    version=get_version(),
    debug=True,
)

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/api")
app.include_router(health_router)
app.include_router(token_router)
app.include_router(version_router, prefix="/api")


def run() -> None:
    uvicorn.run(
        "seizmeia.__main__:app",
        port=config.uvicorn.port,
        host=str(config.uvicorn.host),
        workers=config.uvicorn.workers,
        reload=config.environment.is_dev(),
        loop="asyncio",
    )


if __name__ == "__main__":
    run()
