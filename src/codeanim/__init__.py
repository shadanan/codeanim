#!/usr/bin/env python3
import argparse
import os
from functools import partial
from importlib.metadata import version

from pynput.keyboard import Key

from . import chrome, vscode  # noqa: F401
from .core import codeanim
from .interpolators import Sigmoid, Spring  # noqa: F401
from .parser import CodeAnimBlocks
from .recorder import Recorder

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


def run(args: argparse.Namespace):
    delay.set(end=args.end_delay, tap=args.tap_delay)
    codeanim.keyboard.set_abort_key(args.abort_key)

    verbose: bool = args.verbose
    live: bool = args.live
    blocks = CodeAnimBlocks.parse_file(args.script)

    with codeanim:
        for block in blocks.filter(labels=args.labels, start_label=args.start_label):
            if live:
                wait()
            for expression in block.expressions():
                if verbose:
                    print(expression)
                exec(expression)


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
