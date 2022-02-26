import asyncio
from datetime import timedelta

from time import perf_counter

import pytest

from seizmeia.server.health import ConcurrentHealthCheck


class AsyncHealther:
    def __init__(
        self,
        sleep_time: timedelta,
        live_status: str | None,
        ready_status: str | None,
    ) -> None:
        self.sleep_time = sleep_time
        self.live_status = live_status
        self.ready_status = ready_status

    async def live(self) -> str | None:
        await asyncio.sleep(self.sleep_time.total_seconds())
        return self.live_status

    async def ready(self) -> str | None:
        await asyncio.sleep(self.sleep_time.total_seconds())
        return self.ready_status


@pytest.mark.asyncio
async def test_concurrent_health_check():
    checker1 = AsyncHealther(
        sleep_time=timedelta(seconds=0.1),
        live_status="not alive",
        ready_status="not ready. waiting for something",
    )

    checker2 = AsyncHealther(
        sleep_time=timedelta(seconds=0.5), live_status=None, ready_status=None
    )

    checker3 = AsyncHealther(
        sleep_time=timedelta(seconds=1), live_status=None, ready_status=None
    )

    healthcheck = ConcurrentHealthCheck()
    healthcheck.add("checker1", checker1)
    healthcheck.add("checker2", checker2)
    healthcheck.add("checker3", checker3)

    # testing ready(). it should not take more than the extended computation
    start = perf_counter()
    r = await healthcheck.ready()
    dur = perf_counter() - start

    assert dur == pytest.approx(1, 0.1)
    assert len(r.keys()) == 1
    assert r.get("checker1", None) == checker1.ready_status

    # testing live(). it should not take more than the extended computation
    start = perf_counter()
    r = await healthcheck.live()
    dur = perf_counter() - start

    assert dur == pytest.approx(1, 0.1)

    assert len(r.keys()) == 1
    assert r.get("checker1", None) == checker1.live_status
