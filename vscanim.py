#!/usr/bin/env python3
import argparse
import subprocess
import time


def osascript(cmd: str):
    return subprocess.check_output(["osascript", "-e", cmd]).decode("utf-8").strip()


def activate(app: str):
    osascript(f'tell application "{app}" to activate')


def clear_canvas(*, do_clear_terminal: bool = True, final_delay: bool = True):
    if do_clear_terminal:
        clear_terminal()
    jump(line=3)
    osascript(
        'tell application "System Events" to key code 125 using {command down, shift down}'
    )
    backspace()
    if final_delay:
        delay()


def activate_vscode():
    activate("Visual Studio Code")
    activate_editor()


def activate_terminal():
    osascript('tell application "System Events" to keystroke "`" using {control down}')


def activate_editor():
    osascript('tell application "System Events" to key code 18 using {control down}')


def clear_terminal():
    activate_terminal()
    osascript('tell application "System Events" to keystroke "k" using {command down}')
    activate_editor()


def newline():
    osascript(
        'tell application "System Events" to keystroke return using {command down}'
    )


def delay(seconds: float = 1):
    time.sleep(seconds)


def end():
    osascript('tell application "System Events" to key code 124 using {command down}')


def bottom():
    osascript('tell application "System Events" to key code 125 using {command down}')


def backspace(num: int = 1):
    osascript(
        f"""
        repeat {num} times
            tell application "System Events" to key code 51
        end repeat
        """
    )


def jump(*, line: int, col: int = 1):
    osascript(
        f"""
        tell application "System Events"
            keystroke "p" using {{command down}}
            keystroke ":{line},{col}"
            keystroke return
        end tell
        """
    )


def move(*, lines: int = 0, cols: int = 0):
    if lines < 0:
        osascript(
            f"""
            repeat {-lines} times
                tell application "System Events" to key code 126
            end repeat
            """
        )
    elif lines > 0:
        osascript(
            f"""
            repeat {lines} times
                tell application "System Events" to key code 125
            end repeat
            """
        )

    if cols < 0:
        osascript(
            f"""
            repeat {-cols} times
                tell application "System Events" to key code 123
            end repeat
            """
        )
    elif cols > 0:
        osascript(
            f"""
            repeat {cols} times
                tell application "System Events" to key code 124
            end repeat
            """
        )


def type(text: str, *, return_after: bool = True, final_delay: bool = True):
    escaped_text = text.replace('"', '\\"')
    osascript(f'tell application "System Events" to keystroke "{escaped_text}"')
    if return_after:
        newline()
    if final_delay:
        delay()


def run(final_delay: bool = True):
    osascript(
        'tell application "System Events" to keystroke return using {command down, shift down, option down, control down}'
    )
    if final_delay:
        delay()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "markdown", help="The markdown file containing the animation commands"
    )
    args = parser.parse_args()

    vscanim_lines = []
    is_vscanim = False
    with open(args.markdown) as f:
        lines = f.read().splitlines()
    for line in lines:
        if line.startswith("```vscanim"):
            is_vscanim = True
            continue
        if line.startswith("```"):
            is_vscanim = False
            continue
        if is_vscanim:
            vscanim_lines.append(line)

    activate_vscode()
    for line in vscanim_lines:
        eval(line)


if __name__ == "__main__":
    main()
