from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

from seizmeia.server.health import router as health_router
from seizmeia.server.version import get_version

app = FastAPI()

# including healthcheck routes (/live and /ready)
app.include_router(health_router)


@app.get("/")
async def root() -> Response:
    return JSONResponse({"version": get_version()})
