import asyncio
from typing import Dict, Protocol

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response


class Healther(Protocol):
    """Any object implementing ^ can be checked for health status"""

    async def ready(self) -> str | None:
        ...

    async def live(self) -> str | None:
        ...


class HealthCheckService(Protocol):
    """
    Defines a healthcheck service interface.
    Any service with this interface can be a healthcheck service.
    """

    healthers: Dict[str, Healther] = {}

    def add(self, name: str, healther: Healther) -> None:
        if name in self.healthers.keys():
            raise Exception(f"checker with name {name} already exists")

        self.healthers[name] = healther

    async def ready(self) -> Dict[str, str]:
        ...

    async def live(self) -> Dict[str, str]:
        ...


class ConcurrentHealthCheck(HealthCheckService):
    """
    Implements an asyncio healtcheck service.
    Requesting health status should be as slow as the slowest health provider.
    """

    async def ready(self) -> Dict[str, str]:
        not_ready: Dict[str, str] = {}

        status = await asyncio.gather(
            *[h.ready() for _, h in self.healthers.items()]
        )

        for name, msg in zip(self.healthers.keys(), status):
            if msg:
                not_ready[name] = msg

        return not_ready

    async def live(self) -> Dict[str, str]:
        not_live: Dict[str, str] = {}

        status = await asyncio.gather(
            *[h.live() for _, h in self.healthers.items()]
        )

        for name, msg in zip(self.healthers.keys(), status):
            if msg:
                not_live[name] = msg

        return not_live


router = APIRouter()
healthcheck: HealthCheckService = ConcurrentHealthCheck()


@router.get("/live")
async def live() -> Response:
    """
    The Kubernetes liveness probe detects that the service is no longer serving
    requests and restarts the offending pod.
    """
    not_live = await healthcheck.live()
    if len(not_live.keys()) > 0:
        return JSONResponse(not_live, status.HTTP_503_SERVICE_UNAVAILABLE)

    return JSONResponse(None, status.HTTP_200_OK)


@router.get("/ready")
async def ready() -> Response:
    """
    The Kubernetes readiness probe waits until the app is fully started
    before it allows the to send traffic to the service.
    """
    not_ready = await healthcheck.ready()
    if len(not_ready.keys()) > 0:
        return JSONResponse(not_ready, status.HTTP_503_SERVICE_UNAVAILABLE)

    return JSONResponse(None, status.HTTP_200_OK)
