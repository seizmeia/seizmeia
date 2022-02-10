from seizmeia.server.version import get_version

from fastapi import FastAPI, Depends
from fastapi.responses import Response, JSONResponse

app = FastAPI()


@app.get("/")
async def root() -> Response:
    return JSONResponse({"version": get_version()})
