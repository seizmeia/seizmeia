import uvicorn  # type: ignore


def run() -> None:
    uvicorn.run(
        "seizmeia.server:app",
        http="h11",
        loop="asyncio",
        reload=True,
        workers=1,
    )


if __name__ == "__main__":
    run()
