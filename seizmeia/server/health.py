from typing import Dict, Protocol

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response


class Healther(Protocol):
    """Any object implementing ^ can be checked for health status"""

    async def ready(self) -> str | None:
        ...

    async def health(self) -> str | None:
        ...


class HealthCheckService(Protocol):
    """
    Defines a healthcheck service interface.
    Any service with this interface can be a healthcheck service.
    """

    def add(self, name: str, healther: Healther) -> None:
        ...

    async def ready(self) -> Dict[str, str]:
        ...

    async def health(self) -> Dict[str, str]:
        ...


class __BasicHealthCheck:
    healthers: Dict[str, Healther] = {}

    def add(self, name: str, healther: Healther) -> None:
        if name in self.healthers.keys():
            raise Exception(f"checker with name {name} already exists")

        self.healthers[name] = healther

    async def ready(self) -> Dict[str, str]:
        not_ready: Dict[str, str] = {}

        for name, healther in self.healthers.items():
            msg = await healther.ready()
            if msg is not None:
                not_ready[name] = msg

        return not_ready

    async def health(self) -> Dict[str, str]:
        not_healthy: Dict[str, str] = {}

        for name, healther in self.healthers.items():
            msg = await healther.health()
            if msg is not None:
                not_healthy[name] = msg

        return not_healthy


router = APIRouter()
healthcheck: HealthCheckService = __BasicHealthCheck()


@router.get("/live")
async def live() -> Response:
    """
    The Kubernetes liveness probe detects that the service is no longer serving
    requests and restarts the offending pod.
    """
    not_healthy = await healthcheck.ready()
    if len(not_healthy.keys()) > 0:
        return JSONResponse(not_healthy, status.HTTP_503_SERVICE_UNAVAILABLE)

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
