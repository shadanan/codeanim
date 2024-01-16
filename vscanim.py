#!/usr/bin/env python3
import argparse
import subprocess
import textwrap
import time
from dataclasses import dataclass
from enum import Enum


@dataclass
class Delayer:
    delay: float = 0.5

    def __call__(self):
        time.sleep(self.delay)


delay = Delayer()
verbosity = 0


def escape(text: str):
    return text.replace('"', '\\"')


def osascript(cmd: str) -> str:
    if verbosity > 1:
        print(cmd)
    return subprocess.check_output(["osascript", "-e", cmd]).decode("utf-8").strip()


def activate_vscode():
    osascript(f'tell application "Visual Studio Code" to activate')


def is_vscode_active() -> bool:
    frontmost_process = osascript(
        'tell application "System Events" to '
        "get name of first process whose frontmost is true"
    )
    return frontmost_process == "Electron"


class KeyCode(Enum):
    ONE = 18
    RETURN = 36
    BACKSPACE = 51
    ESCAPE = 53
    LEFT = 123
    RIGHT = 124
    DOWN = 125
    UP = 126


class Modifier(Enum):
    COMMAND = "command down"
    SHIFT = "shift down"
    OPTION = "option down"
    CONTROL = "control down"


@dataclass
class KeyStroke:
    code: KeyCode | str
    modifiers: list[Modifier] | None = None

    def __str__(self) -> str:
        cmd = []
        if isinstance(self.code, KeyCode):
            cmd += ["key code", str(self.code.value)]
        else:
            cmd += ["keystroke", f'"{escape(self.code)}"']
        if self.modifiers is not None:
            cmd += ["using", "{", ", ".join([m.value for m in self.modifiers]), "}"]
        return " ".join(cmd)


def command(cmd: str):
    return [
        KeyStroke("p", modifiers=[Modifier.COMMAND]),
        KeyStroke(cmd),
        KeyStroke(KeyCode.RETURN),
    ]


def indent(strokes: list[KeyStroke] | list[str] | list[KeyStroke | str]) -> list[str]:
    return [textwrap.indent(str(s), "  ") for s in strokes]


def repeat(lines: list[KeyStroke], num: int) -> list[str]:
    return [f"repeat {num} times"] + indent(lines) + ["end repeat"]


def send(lines: list[KeyStroke] | list[str] | list[KeyStroke | str]):
    if not is_vscode_active():
        raise Exception("Aborting execution because VS Code is no longer active")
    cmd = ['tell application "System Events"'] + indent(lines) + ["end tell"]
    osascript("\n".join(cmd))


def newline():
    send([KeyStroke(KeyCode.RETURN, modifiers=[Modifier.COMMAND])])


def type(text: str, *, return_after: bool = True, final_delay: bool = True):
    send([KeyStroke(text)])
    if return_after:
        newline()
    if final_delay:
        delay()


def backspace(num: int = 1):
    send(repeat([KeyStroke(KeyCode.BACKSPACE)], num))


def jump(*, line: int, col: int = 1):
    send(command(f":{line},{col}"))


def end():
    send([KeyStroke(KeyCode.RIGHT, modifiers=[Modifier.COMMAND])])


def bottom():
    send([KeyStroke(KeyCode.DOWN, modifiers=[Modifier.COMMAND])])


def move(*, lines: int = 0, cols: int = 0):
    if lines < 0:
        send(repeat([KeyStroke(KeyCode.UP)], -lines))
    elif lines > 0:
        send(repeat([KeyStroke(KeyCode.DOWN)], lines))

    if cols < 0:
        send(repeat([KeyStroke(KeyCode.LEFT)], -cols))
    elif cols > 0:
        send(repeat([KeyStroke(KeyCode.RIGHT)], cols))


def focus_terminal():
    send([KeyStroke("`", modifiers=[Modifier.CONTROL])])


def focus_editor():
    send([KeyStroke(KeyCode.ONE, modifiers=[Modifier.CONTROL])])


def clear_terminal():
    focus_terminal()
    send([KeyStroke("k", modifiers=[Modifier.COMMAND])])
    focus_editor()


def clear_below(line: int):
    jump(line=line)
    send([KeyStroke(KeyCode.DOWN, modifiers=[Modifier.COMMAND, Modifier.SHIFT])])
    backspace()


def clear_canvas(
    *, line: int = 2, do_clear_terminal: bool = True, final_delay: bool = True
):
    if do_clear_terminal:
        clear_terminal()
    clear_below(line)
    if final_delay:
        delay()


def run(final_delay: bool = True):
    send(
        [
            KeyStroke(
                KeyCode.RETURN,
                modifiers=[
                    Modifier.COMMAND,
                    Modifier.SHIFT,
                    Modifier.OPTION,
                    Modifier.CONTROL,
                ],
            )
        ]
    )
    if final_delay:
        delay()


def main():
    global verbosity

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "markdown",
        help="The markdown file containing the animation commands",
    )
    parser.add_argument(
        "--start-label",
        help="The label to start at",
    )
    parser.add_argument(
        "--stop-label",
        help="The label to stop at",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="The default delay between commands",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity",
    )
    args = parser.parse_args()
    verbosity = args.verbose

    vscanim_lines = []
    is_vscanim = False
    is_included = args.start_label is None
    with open(args.markdown) as f:
        lines = f.read().splitlines()
    for line in lines:
        tokens = line.strip().split()
        if len(tokens) == 0:
            continue
        if tokens[0] == "```vscanim":
            is_vscanim = True
            if len(tokens) >= 2:
                if tokens[1] == args.start_label:
                    is_included = True
                elif tokens[1] == args.stop_label:
                    is_included = False
            continue
        if tokens[0] == "```":
            is_vscanim = False
            continue
        if is_vscanim and is_included:
            vscanim_lines.append(line)

    delay.delay = args.delay
    activate_vscode()
    for line in vscanim_lines:
        if verbosity > 0:
            print(f"> VscAnim Command: {line}")
        eval(line)


if __name__ == "__main__":
    main()
