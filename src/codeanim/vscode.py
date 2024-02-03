import pyperclip
from pynput.keyboard import Key

from .core import backspace, codeanim, keyboard, no_delays, osascript, tap, write


def activate():
    osascript(f'tell application "Visual Studio Code" to activate')


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
