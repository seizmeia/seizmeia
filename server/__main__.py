from server import get_version

from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.requests import Request
from starlette.routing import Route
import uvicorn  # type: ignore


async def root(request: Request) -> Response:
    return JSONResponse({"version": get_version()})


app = Starlette(
    debug=True,
    routes=[
        Route("/", root),
    ],
)


def run() -> None:
    uvicorn.run(app, http="h11", loop="asyncio")


if __name__ == "__main__":
    run()
