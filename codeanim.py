#!/usr/bin/env python3
import argparse
import ast
import subprocess
import time
from contextlib import contextmanager
from dataclasses import dataclass, field

import pyperclip
from pynput.keyboard import Controller, Key

keyboard = Controller()


def osascript(cmd: str) -> str:
    return subprocess.check_output(["osascript", "-e", cmd]).decode("utf-8").strip()


def activate_vscode():
    osascript(f'tell application "Visual Studio Code" to activate')


@dataclass
class Delayer:
    tap: float = 0.02
    keys: dict[str | Key, float] = field(default_factory=dict)
    end: float = 0.5


delayer = Delayer()


def set_delays(
    *,
    tap: float | None = None,
    keys: dict[str | Key, float] | None = None,
    end: float | None = None,
):
    prev_tap, delayer.tap = delayer.tap, delayer.tap if tap is None else tap
    prev_keys, delayer.keys = delayer.keys, delayer.keys if keys is None else keys
    prev_end, delayer.end = delayer.end, delayer.end if end is None else end
    return prev_tap, prev_keys, prev_end


@contextmanager
def delays(
    *,
    tap: float | None = None,
    keys: dict[str | Key, float] | None = None,
    end: float | None = None,
):
    prev_tap, prev_keys, prev_end = set_delays(tap=tap, keys=keys, end=end)
    yield
    delayer.tap, delayer.keys, delayer.end = prev_tap, prev_keys, prev_end


def no_delays():
    return delays(tap=0, keys={}, end=0)


def tap(key: str | Key, *, modifiers: list[str | Key] = []):
    for modifier in modifiers:
        keyboard.press(modifier)
    keyboard.tap(key)
    for modifier in modifiers:
        keyboard.release(modifier)
    time.sleep(delayer.keys.get(key, delayer.tap))


def delay(end: float | None = None):
    end = delayer.end if end is None else end
    time.sleep(end)


def codeanim(func):
    def codeanim_func(*args, **kwargs):
        func(*args, **kwargs)
        delay()

    return codeanim_func


@codeanim
def paste(text: str, *, paste_delay: float = 0.5):
    pyperclip.copy(text)
    tap("v", modifiers=[Key.cmd])
    time.sleep(paste_delay)  # Need to wait for the paste to finish


@codeanim
def write(text: str):
    for char in text:
        if char == "\n":
            tap(Key.enter)
        elif char == "\t":
            tap(Key.tab)
        elif len(char.encode("utf-8")) != 1:
            paste(char)
        else:
            tap(char)


@codeanim
def palette(cmd: str):
    tap("p", modifiers=[Key.cmd])
    write(cmd)
    tap(Key.enter)


@codeanim
def newline(line: int = 0, *, above: bool = False):
    if line > 0:
        with no_delays():
            jump(line)
        tap(Key.enter, modifiers=[Key.cmd, Key.shift])
    else:
        tap(Key.enter, modifiers=[Key.cmd, Key.shift] if above else [Key.cmd])


@codeanim
def backspace(num: int = 1):
    for _ in range(num):
        tap(Key.backspace)


@codeanim
def jump(line: int, col: int = 1):
    pyperclip.copy(f":{line},{col}")
    with keyboard.pressed(Key.cmd):
        keyboard.tap("p")
        keyboard.tap("v")
    keyboard.tap(Key.enter)


@codeanim
def move(*, lines: int = 0, cols: int = 0, select: bool = False):
    if lines < 0:
        for _ in range(-lines):
            tap(Key.up, modifiers=[Key.shift] if select else [])
    elif lines > 0:
        for _ in range(lines):
            tap(Key.down, modifiers=[Key.shift] if select else [])
    if cols < 0:
        for _ in range(-cols):
            tap(Key.left, modifiers=[Key.shift] if select else [])
    elif cols > 0:
        for _ in range(cols):
            tap(Key.right, modifiers=[Key.shift] if select else [])


@codeanim
def end(*, select: bool = False):
    tap(Key.right, modifiers=[Key.cmd, Key.shift] if select else [Key.cmd])


@codeanim
def bottom(*, select: bool = False):
    tap(Key.down, modifiers=[Key.cmd, Key.shift] if select else [Key.cmd])


@codeanim
def focus(file: str):
    palette(file)


@codeanim
def focus_terminal():
    tap("`", modifiers=[Key.ctrl])


@codeanim
def focus_editor():
    tap("1", modifiers=[Key.ctrl])


@codeanim
def toggle_panel():
    tap("j", modifiers=[Key.cmd])


@codeanim
def toggle_primary_sidebar():
    tap("b", modifiers=[Key.cmd])


@codeanim
def clear_terminal():
    focus_terminal()
    tap("k", modifiers=[Key.cmd])
    focus_editor()


@codeanim
def clear_editor():
    tap("a", modifiers=[Key.cmd])
    backspace()


@codeanim
def clear_below(line: int):
    jump(line)
    tap(Key.down, modifiers=[Key.cmd, Key.shift])
    backspace()


@codeanim
def run():
    tap(Key.enter, modifiers=[Key.cmd, Key.shift, Key.ctrl, Key.alt])


def parse(path: str, labels: list[str] | None) -> list[str]:
    with open(path) as f:
        lines = f.read().splitlines()

    codeanim_lines = []
    is_codeanim = False
    for line in lines:
        if line.startswith("```python"):
            tokens = line.strip().split()
            codeanim = len(tokens) > 1 and tokens[1] == "codeanim"
            label = tokens[2] if len(tokens) > 2 else ""
            is_codeanim = codeanim and (labels is None or label in labels)
            continue
        if line == "```":
            is_codeanim = False
            continue
        if is_codeanim:
            codeanim_lines.append(line)

    module = ast.parse("\n".join(codeanim_lines))
    expressions = []
    for node in module.body:
        start = node.lineno - 1
        end = node.end_lineno if node.end_lineno is not None else start
        expressions.append("\n".join(codeanim_lines[start:end]))
    return expressions


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

    expressions = parse(args.markdown, args.labels)
    activate_vscode()
    for expression in expressions:
        if args.verbose:
            print(expression)
        exec(expression)


if __name__ == "__main__":
    main()
