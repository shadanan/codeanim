from pynput.keyboard import Key

from .core import CodeAnim

APP_NAME = "Code"


@CodeAnim.cmd
def open(ca: CodeAnim, path: str):
    if path.endswith(".code-workspace"):
        ca.shell.open(path)
    else:
        ca.shell.code(path)


@CodeAnim.cmd
def activate(ca: CodeAnim):
    ca.shell.activate(APP_NAME)


@CodeAnim.cmd
def resize(ca: CodeAnim, position: tuple[int, int], size: tuple[int, int]):
    ca.shell.resize(APP_NAME, position, size)


@CodeAnim.cmd
def palette(ca: CodeAnim, cmd: str):
    ca.tap("p", modifiers=[Key.cmd])
    ca.write(cmd)
    ca.tap(Key.enter)


@CodeAnim.cmd
def newline(ca: CodeAnim, line: int = 0, *, above: bool = False):
    if line > 0:
        jump(line)
        ca.tap(Key.enter, modifiers=[Key.cmd, Key.shift])
    else:
        ca.tap(Key.enter, modifiers=[Key.cmd, Key.shift] if above else [Key.cmd])


@CodeAnim.cmd
def jump(ca: CodeAnim, line: int, col: int = 1):
    ca.tap("p", modifiers=[Key.cmd])
    ca.paste(f":{line},{col}", paste_delay=0)
    ca.tap(Key.enter)


@CodeAnim.cmd
def move(ca: CodeAnim, *, lines: int = 0, cols: int = 0, select: bool = False):
    if lines < 0:
        for _ in range(-lines):
            ca.tap(Key.up, modifiers=[Key.shift] if select else [])
    elif lines > 0:
        for _ in range(lines):
            ca.tap(Key.down, modifiers=[Key.shift] if select else [])
    if cols < 0:
        for _ in range(-cols):
            ca.tap(Key.left, modifiers=[Key.shift] if select else [])
    elif cols > 0:
        for _ in range(cols):
            ca.tap(Key.right, modifiers=[Key.shift] if select else [])


@CodeAnim.cmd
def end(ca: CodeAnim, *, select: bool = False):
    ca.tap(Key.right, modifiers=[Key.cmd, Key.shift] if select else [Key.cmd])


@CodeAnim.cmd
def bottom(ca: CodeAnim, *, select: bool = False):
    ca.tap(Key.down, modifiers=[Key.cmd, Key.shift] if select else [Key.cmd])


@CodeAnim.cmd
def new_file(ca: CodeAnim):
    ca.tap("n", modifiers=[Key.cmd])


@CodeAnim.cmd
def save(ca: CodeAnim, file: str | None = None):
    if file is None:
        ca.tap("s", modifiers=[Key.cmd])
    else:
        ca.tap("s", modifiers=[Key.cmd, Key.shift])
        ca.delay.pause(0.5)
        ca.write(file)
        ca.tap(Key.enter)


@CodeAnim.cmd
def focus(_, file: str):
    palette(file)


@CodeAnim.cmd
def focus_editor(ca: CodeAnim):
    ca.tap("1", modifiers=[Key.ctrl])


@CodeAnim.cmd
def toggle_terminal(ca: CodeAnim):
    ca.tap("`", modifiers=[Key.ctrl])


@CodeAnim.cmd
def toggle_panel(ca: CodeAnim):
    ca.tap("j", modifiers=[Key.cmd])


@CodeAnim.cmd
def toggle_primary_sidebar(ca: CodeAnim):
    ca.tap("b", modifiers=[Key.cmd])


@CodeAnim.cmd
def clear_terminal(ca: CodeAnim):
    toggle_terminal()
    ca.tap("k", modifiers=[Key.cmd])
    focus_editor()


@CodeAnim.cmd
def clear_editor(ca: CodeAnim):
    ca.tap("a", modifiers=[Key.cmd])
    ca.backspace()


@CodeAnim.cmd
def clear_below(ca: CodeAnim, line: int):
    jump(line)
    ca.tap(Key.down, modifiers=[Key.cmd, Key.shift])
    ca.backspace()
