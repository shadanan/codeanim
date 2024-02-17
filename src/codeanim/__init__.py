#!/usr/bin/env python3
import argparse
import os

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
from .monitor import wait  # noqa: F401


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
    parser.add_argument(
        "--tap-delay",
        type=float,
        default=os.environ.get("CODE_ANIM_TAP_DELAY"),
        help="The delay between keyboard taps",
    )
    parser.add_argument(
        "--end-delay",
        type=float,
        default=os.environ.get("CODE_ANIM_END_DELAY"),
        help="The delay at the end of each animation command",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Insert wait after each codeanim block",
    )
    args = parser.parse_args()

    set_delays(tap=args.tap_delay, end=args.end_delay)

    expressions = markdown.parse(args.markdown, args.labels, args.live)
    for expression in expressions:
        if args.verbose:
            print(expression)
        exec(expression)


if __name__ == "__main__":
    main()
