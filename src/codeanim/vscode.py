import pyperclip
from pynput.keyboard import Key

from . import core


def activate():
    core.osascript(f'tell application "Visual Studio Code" to activate')


@core.codeanim
def palette(cmd: str):
    core.tap("p", modifiers=[Key.cmd])
    core.write(cmd)
    core.tap(Key.enter)


@core.codeanim
def newline(line: int = 0, *, above: bool = False):
    if line > 0:
        with core.no_delays():
            jump(line)
        core.tap(Key.enter, modifiers=[Key.cmd, Key.shift])
    else:
        core.tap(Key.enter, modifiers=[Key.cmd, Key.shift] if above else [Key.cmd])


@core.codeanim
def jump(line: int, col: int = 1):
    pyperclip.copy(f":{line},{col}")
    with core.keyboard.pressed(Key.cmd):
        core.keyboard.tap("p")
        core.keyboard.tap("v")
    core.keyboard.tap(Key.enter)


@core.codeanim
def move(*, lines: int = 0, cols: int = 0, select: bool = False):
    if lines < 0:
        for _ in range(-lines):
            core.tap(Key.up, modifiers=[Key.shift] if select else [])
    elif lines > 0:
        for _ in range(lines):
            core.tap(Key.down, modifiers=[Key.shift] if select else [])
    if cols < 0:
        for _ in range(-cols):
            core.tap(Key.left, modifiers=[Key.shift] if select else [])
    elif cols > 0:
        for _ in range(cols):
            core.tap(Key.right, modifiers=[Key.shift] if select else [])


@core.codeanim
def end(*, select: bool = False):
    core.tap(Key.right, modifiers=[Key.cmd, Key.shift] if select else [Key.cmd])


@core.codeanim
def bottom(*, select: bool = False):
    core.tap(Key.down, modifiers=[Key.cmd, Key.shift] if select else [Key.cmd])


@core.codeanim
def focus(file: str):
    palette(file)


@core.codeanim
def focus_terminal():
    core.tap("`", modifiers=[Key.ctrl])


@core.codeanim
def focus_editor():
    core.tap("1", modifiers=[Key.ctrl])


@core.codeanim
def toggle_panel():
    core.tap("j", modifiers=[Key.cmd])


@core.codeanim
def toggle_primary_sidebar():
    core.tap("b", modifiers=[Key.cmd])


@core.codeanim
def clear_terminal():
    focus_terminal()
    core.tap("k", modifiers=[Key.cmd])
    focus_editor()


@core.codeanim
def clear_editor():
    core.tap("a", modifiers=[Key.cmd])
    core.backspace()


@core.codeanim
def clear_below(line: int):
    jump(line)
    core.tap(Key.down, modifiers=[Key.cmd, Key.shift])
    core.backspace()


@core.codeanim
def run():
    core.tap(Key.enter, modifiers=[Key.cmd, Key.shift, Key.ctrl, Key.alt])
