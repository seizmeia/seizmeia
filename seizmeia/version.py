from __future__ import annotations

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


if __name__ == "__main__":
    import sys

    ascii_beer = ".~~~~.\n" "i====i_\n" "|cccc|_)\n" "|cccc|\n" "`-==-'\n"

    # sys.stdout.write(ascii_beer)
    sys.stdout.write(get_version())
    sys.exit(0)
