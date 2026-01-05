#!/usr/bin/env python3
import argparse
import os
from functools import partial
from importlib.metadata import version
from typing import Any, Sequence

from pynput.keyboard import Key

from codeanim.chrome import Chrome
from codeanim.vscode import VSCode

from .core import CodeAnim
from .interpolators import Sigmoid, Spring
from .parser import CodeAnimBlocks
from .recorder import Recorder

__all__ = [
    "CodeAnim",
    "Key",
    "Chrome",
    "VSCode",
    "Sigmoid",
    "Spring",
]


class VersionAction(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ):
        print(version("codeanim"))
        parser.exit()


def run(args: argparse.Namespace):
    ca = CodeAnim()

    ca.delay.set(end=args.end_delay, tap=args.tap_delay)
    ca.keyboard.set_abort_key(args.abort_key)

    verbose: bool = args.verbose
    live: bool = args.live
    blocks = CodeAnimBlocks.parse_file(args.script)

    with ca:
        for block in blocks.filter(labels=args.labels, start_label=args.start_label):
            if live:
                ca.wait()
            for expression in block.expressions():
                if verbose:
                    print(expression)
                exec(
                    expression,
                    locals={
                        "chrome": Chrome(ca),
                        "vscode": VSCode(ca),
                        "backspace": ca.backspace,
                        "click": ca.click,
                        "delay": ca.delay,
                        "drag": ca.drag,
                        "move": ca.move,
                        "paste": ca.paste,
                        "pause": ca.pause,
                        "scroll": ca.scroll,
                        "tap": ca.tap,
                        "wait": ca.wait,
                        "write": ca.write,
                    },
                )


def record(args: argparse.Namespace):
    recorder = Recorder(abort_key=args.abort_key, verbose=args.verbose)
    with recorder:
        recorder.wait()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print the animation commands as they are executed or recorded",
    )

    parser.add_argument(
        "--abort-key",
        default=Key.shift_r,
        type=partial(getattr, Key),
        help="Abort execution when this key is pressed",
    )

    subparsers = parser.add_subparsers(title="subcommands", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.set_defaults(cmd=run)
    run_parser.add_argument(
        "script",
        help="The markdown or python file containing the animation commands",
    )
    run_parser.add_argument(
        "--labels",
        nargs="+",
        type=set,
        default=None,
        help="The list of labeled CodeAnim blocks to execute",
    )
    run_parser.add_argument(
        "--start-label",
        default=None,
        help="The label of the CodeAnim block to start from",
    )
    run_parser.add_argument(
        "--tap-delay",
        type=float,
        default=os.environ.get("CODE_ANIM_TAP_DELAY"),
        help="The delay between keyboard taps",
    )
    run_parser.add_argument(
        "--end-delay",
        type=float,
        default=os.environ.get("CODE_ANIM_END_DELAY"),
        help="The delay at the end of each animation command",
    )
    run_parser.add_argument(
        "--live",
        action="store_true",
        help="Insert wait after each codeanim block",
    )
    run_parser.add_argument(
        "--version",
        nargs=0,
        action=VersionAction,
        help="Print the version information and exit",
    )

    record_parser = subparsers.add_parser("record")
    record_parser.set_defaults(cmd=record)

    args = parser.parse_args()
    args.cmd(args)


if __name__ == "__main__":
    main()
