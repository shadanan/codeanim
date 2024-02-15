from pynput.keyboard import Key

from . import core

APP_NAME = "Google Chrome"


@core.codeanim
def activate():
    core.activate(APP_NAME)


@core.codeanim
def resize(position: tuple[int, int], size: tuple[int, int]):
    core.resize(APP_NAME, position, size)


@core.codeanim
def navigate(url: str):
    with core.no_final_delay():
        core.tap("l", modifiers=[Key.cmd])
        core.write(url)
    core.tap(Key.enter)


@core.codeanim
def back():
    core.tap(Key.left, modifiers=[Key.cmd])


@core.codeanim
def forward():
    core.tap(Key.right, modifiers=[Key.cmd])


@core.codeanim
def new_tab():
    core.tap("t", modifiers=[Key.cmd])
    core.tap(Key.esc)


@core.codeanim
def previous_tab(times: int = 1):
    for _ in range(times):
        core.tap("{", modifiers=[Key.cmd, Key.shift])


@core.codeanim
def next_tab(times: int = 1):
    for _ in range(times):
        core.tap("}", modifiers=[Key.cmd, Key.shift])


@core.codeanim
def close_tab():
    core.tap("w", modifiers=[Key.cmd])


@core.codeanim
def new_window():
    core.tap("n", modifiers=[Key.cmd])
    core.tap(Key.esc)


@core.codeanim
def close_window():
    core.tap("w", modifiers=[Key.cmd, Key.shift])


@core.codeanim
def refresh():
    core.tap("r", modifiers=[Key.cmd])


@core.codeanim
def toggle_devtools():
    core.tap("i", modifiers=[Key.cmd, Key.alt])


@core.codeanim
def prev_devtools_panel(times: int = 1):
    for _ in range(times):
        core.tap("[", modifiers=[Key.cmd])


@core.codeanim
def next_devtools_panel(times: int = 1):
    for _ in range(times):
        core.tap("]", modifiers=[Key.cmd])
