#!/usr/bin/env python3
import argparse
import os
from functools import partial
from importlib.metadata import version

from pynput.keyboard import Key  # noqa: F401
from pynput.mouse import Button  # noqa: F401

from . import chrome, vscode  # noqa: F401
from .core import codeanim
from .interpolators import Sigmoid, Spring  # noqa: F401
from .markdown import parse

# Public API
backspace = codeanim.backspace
click = codeanim.click
delay = codeanim.delay
drag = codeanim.drag
move = codeanim.move
paste = codeanim.paste
pause = codeanim.delay.pause
scroll = codeanim.scroll
tap = codeanim.tap
wait = codeanim.wait
write = codeanim.write


class VersionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(version("codeanim"))
        parser.exit()


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
    parser.add_argument(
        "--abort-key",
        default=Key.shift_r,
        type=partial(getattr, Key),
        help="Abort CodeAnim execution when this key is pressed",
    )
    parser.add_argument(
        "--version",
        nargs=0,
        action=VersionAction,
        help="Print the version information and exit",
    )
    args = parser.parse_args()

    delay.set(end=args.end_delay, tap=args.tap_delay)
    codeanim.keyboard.set_abort_key(args.abort_key)

    with codeanim:
        expressions = parse(
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
