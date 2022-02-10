import subprocess

__version__ = "0.0.1"


def get_version() -> str:
    return f"{__version__}-{__get_git_description()}"


def __get_git_description() -> str:
    return (
        subprocess.check_output(["git", "describe", "--dirty", "--always"])
        .decode("ascii")
        .strip()
    )
