import uvicorn  # type: ignore


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
