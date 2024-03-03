#!/usr/bin/env python3
import argparse
import os

from . import chrome, core, markdown, vscode  # noqa: F401
from .core import codeanim

# Public API
Key = core.Key
backspace = codeanim.backspace
delay = codeanim.delay
pause = codeanim.delay.pause
paste = codeanim.paste
tap = codeanim.tap
wait = codeanim.wait
write = codeanim.write


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
        "--start-label",
        default=None,
        help="The label of the CodeAnim block to start from",
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

    delay.set(end=args.end_delay, tap=args.tap_delay)

    with codeanim:
        expressions = markdown.parse(
            args.markdown,
            live=args.live,
            labels=args.labels,
            start_label=args.start_label,
        )
        for expression in expressions:
            if args.verbose:
                print(expression)
            exec(expression)


if __name__ == "__main__":
    main()
