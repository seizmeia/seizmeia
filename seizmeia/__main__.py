from __future__ import annotations

import uvicorn  # type: ignore
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from seizmeia.db import Base, engine
from seizmeia.health import router as health_router
from seizmeia.settings import Settings
from seizmeia.user.routes import router as user_router
from seizmeia.user.routes import token_router
from seizmeia.version import get_version
from seizmeia.version import router as version_router

config = Settings()

app = FastAPI(
    title="Seizmeia 🍺",
    description="A credit management tool for a beer tap.",
    version=get_version(),
    debug=True,
)

origins = ["http://localhost:3000", "http://localhost:80", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")

Base.metadata.create_all(bind=engine)

router.include_router(version_router)
router.include_router(user_router)

app.include_router(health_router)
app.include_router(token_router)
app.include_router(router)


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
