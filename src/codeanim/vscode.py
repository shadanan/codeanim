from pynput.keyboard import Key

from .core import CodeAnim

APP_NAME = "Code"


class VSCode:
    """VS Code automation commands."""

    def __init__(self, ca: CodeAnim):
        self.ca = ca

    def open(self, path: str):
        @self.ca.register
        def _open():
            if path.endswith(".code-workspace"):
                self.ca.shell.open(path)
            else:
                self.ca.shell.code(path)

        return _open()

    def activate(self):
        @self.ca.register
        def _activate():
            self.ca.shell.activate(APP_NAME)

        return _activate()

    def resize(self, position: tuple[int, int], size: tuple[int, int]):
        @self.ca.register
        def _resize():
            self.ca.shell.resize(APP_NAME, position, size)

        return _resize()

    def palette(self, cmd: str):
        @self.ca.register
        def _palette():
            self.ca.tap("p", modifiers=[Key.cmd])
            self.ca.write(cmd)
            self.ca.tap(Key.enter)

        return _palette()

    def newline(self, line: int = 0, *, above: bool = False):
        @self.ca.register
        def _newline():
            if line > 0:
                self.jump(line)
                self.ca.tap(Key.enter, modifiers=[Key.cmd, Key.shift])
            else:
                self.ca.tap(
                    Key.enter, modifiers=[Key.cmd, Key.shift] if above else [Key.cmd]
                )

        return _newline()

    def jump(self, line: int, col: int = 1):
        @self.ca.register
        def _jump():
            self.ca.tap("p", modifiers=[Key.cmd])
            self.ca.paste(f":{line},{col}", paste_delay=0)
            self.ca.tap(Key.enter)

        return _jump()

    def move(self, *, lines: int = 0, cols: int = 0, select: bool = False):
        @self.ca.register
        def _move():
            if lines < 0:
                for _ in range(-lines):
                    self.ca.tap(Key.up, modifiers=[Key.shift] if select else [])
            elif lines > 0:
                for _ in range(lines):
                    self.ca.tap(Key.down, modifiers=[Key.shift] if select else [])
            if cols < 0:
                for _ in range(-cols):
                    self.ca.tap(Key.left, modifiers=[Key.shift] if select else [])
            elif cols > 0:
                for _ in range(cols):
                    self.ca.tap(Key.right, modifiers=[Key.shift] if select else [])

        return _move()

    def end(self, *, select: bool = False):
        @self.ca.register
        def _end():
            self.ca.tap(
                Key.right, modifiers=[Key.cmd, Key.shift] if select else [Key.cmd]
            )

        return _end()

    def bottom(self, *, select: bool = False):
        @self.ca.register
        def _bottom():
            self.ca.tap(
                Key.down, modifiers=[Key.cmd, Key.shift] if select else [Key.cmd]
            )

        return _bottom()

    def new_file(self):
        @self.ca.register
        def _new_file():
            self.ca.tap("n", modifiers=[Key.cmd])

        return _new_file()

    def save(self, file: str | None = None):
        @self.ca.register
        def _save():
            if file is None:
                self.ca.tap("s", modifiers=[Key.cmd])
            else:
                self.ca.tap("s", modifiers=[Key.cmd, Key.shift])
                self.ca.delay.pause(0.5)
                self.ca.write(file)
                self.ca.tap(Key.enter)

        return _save()

    def focus(self, file: str):
        @self.ca.register
        def _focus():
            self.palette(file)

        return _focus()

    def focus_editor(self):
        @self.ca.register
        def _focus_editor():
            self.ca.tap("1", modifiers=[Key.ctrl])

        return _focus_editor()

    def toggle_terminal(self):
        @self.ca.register
        def _toggle_terminal():
            self.ca.tap("`", modifiers=[Key.ctrl])

        return _toggle_terminal()

    def toggle_panel(self):
        @self.ca.register
        def _toggle_panel():
            self.ca.tap("j", modifiers=[Key.cmd])

        return _toggle_panel()

    def toggle_primary_sidebar(self):
        @self.ca.register
        def _toggle_primary_sidebar():
            self.ca.tap("b", modifiers=[Key.cmd])

        return _toggle_primary_sidebar()

    def clear_terminal(self):
        @self.ca.register
        def _clear_terminal():
            self.toggle_terminal()
            self.ca.tap("k", modifiers=[Key.cmd])
            self.focus_editor()

        return _clear_terminal()

    def clear_editor(self):
        @self.ca.register
        def _clear_editor():
            self.ca.tap("a", modifiers=[Key.cmd])
            self.ca.backspace()

        return _clear_editor()

    def clear_below(self, line: int):
        @self.ca.register
        def _clear_below():
            self.jump(line)
            self.ca.tap(Key.down, modifiers=[Key.cmd, Key.shift])
            self.ca.backspace()

        return _clear_below()
