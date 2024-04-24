from pynput.keyboard import Key

from .core import CodeAnim

APP_NAME = "Google Chrome"


@CodeAnim.cmd
def activate(ca: CodeAnim):
    ca.shell.activate(APP_NAME)


@CodeAnim.cmd
def resize(ca: CodeAnim, position: tuple[int, int], size: tuple[int, int]):
    ca.shell.resize(APP_NAME, position, size)


@CodeAnim.cmd
def navigate(ca: CodeAnim, url: str):
    ca.tap("l", modifiers=[Key.cmd])
    ca.write(url)
    ca.tap(Key.enter)


@CodeAnim.cmd
def back(ca: CodeAnim):
    ca.tap(Key.left, modifiers=[Key.cmd])


@CodeAnim.cmd
def forward(ca: CodeAnim):
    ca.tap(Key.right, modifiers=[Key.cmd])


@CodeAnim.cmd
def new_tab(ca: CodeAnim):
    ca.tap("t", modifiers=[Key.cmd])
    ca.tap(Key.esc)


@CodeAnim.cmd
def previous_tab(ca: CodeAnim, times: int = 1):
    for _ in range(times):
        ca.tap("{", modifiers=[Key.cmd, Key.shift])


@CodeAnim.cmd
def next_tab(ca: CodeAnim, times: int = 1):
    for _ in range(times):
        ca.tap("}", modifiers=[Key.cmd, Key.shift])


@CodeAnim.cmd
def close_tab(ca: CodeAnim):
    ca.tap("w", modifiers=[Key.cmd])


@CodeAnim.cmd
def new_window(ca: CodeAnim):
    ca.tap("n", modifiers=[Key.cmd])
    ca.tap(Key.esc)


@CodeAnim.cmd
def close_window(ca: CodeAnim):
    ca.tap("w", modifiers=[Key.cmd, Key.shift])


@CodeAnim.cmd
def refresh(ca: CodeAnim):
    ca.tap("r", modifiers=[Key.cmd])


@CodeAnim.cmd
def toggle_devtools(ca: CodeAnim):
    ca.tap("i", modifiers=[Key.cmd, Key.alt])


@CodeAnim.cmd
def prev_devtools_panel(ca: CodeAnim, times: int = 1):
    for _ in range(times):
        ca.tap("[", modifiers=[Key.cmd])


@CodeAnim.cmd
def next_devtools_panel(ca: CodeAnim, times: int = 1):
    for _ in range(times):
        ca.tap("]", modifiers=[Key.cmd])
