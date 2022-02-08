import subprocess

__version__ = "0.0.1"


def get_git_description() -> str:
    return (
        subprocess.check_output(["git", "describe", "--dirty", "--always"])
        .decode("ascii")
        .strip()
    )


def get_version() -> str:
    return f"{__version__}-{get_git_description()}"
