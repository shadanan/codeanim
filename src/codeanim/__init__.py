#!/usr/bin/env python3
import argparse

from . import chrome, core, markdown, vscode  # noqa: F401
from .core import (  # noqa: F401
    backspace,
    delay,
    delays,
    no_delays,
    paste,
    set_delays,
    tap,
    write,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "markdown",
        help="The markdown file containing the animation commands",
    )
    parser.add_argument(
        "--labels",
        nargs="+",
        default=None,
        help="The list of labeled CodeAnim blocks to execute",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print the animation commands as they are executed",
    )
    args = parser.parse_args()

    expressions = markdown.parse(args.markdown, args.labels)
    for expression in expressions:
        if args.verbose:
            print(expression)
        exec(expression)


if __name__ == "__main__":
    main()
