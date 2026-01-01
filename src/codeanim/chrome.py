from pynput.keyboard import Key

from .core import CodeAnim

APP_NAME = "Google Chrome"


class Chrome:
    """Chrome automation commands."""

    def __init__(self, ca: CodeAnim):
        self.ca = ca

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

    def navigate(self, url: str):
        @self.ca.register
        def _navigate():
            self.ca.tap("l", modifiers=[Key.cmd])
            self.ca.write(url)
            self.ca.tap(Key.enter)

        return _navigate()

    def back(self):
        @self.ca.register
        def _back():
            self.ca.tap(Key.left, modifiers=[Key.cmd])

        return _back()

    def forward(self):
        @self.ca.register
        def _forward():
            self.ca.tap(Key.right, modifiers=[Key.cmd])

        return _forward()

    def new_tab(self):
        @self.ca.register
        def _new_tab():
            self.ca.tap("t", modifiers=[Key.cmd])
            self.ca.tap(Key.esc)

        return _new_tab()

    def previous_tab(self, times: int = 1):
        @self.ca.register
        def _previous_tab():
            for _ in range(times):
                self.ca.tap("{", modifiers=[Key.cmd, Key.shift])

        return _previous_tab()

    def next_tab(self, times: int = 1):
        @self.ca.register
        def _next_tab():
            for _ in range(times):
                self.ca.tap("}", modifiers=[Key.cmd, Key.shift])

        return _next_tab()

    def close_tab(self):
        @self.ca.register
        def _close_tab():
            self.ca.tap("w", modifiers=[Key.cmd])

        return _close_tab()

    def new_window(self):
        @self.ca.register
        def _new_window():
            self.ca.tap("n", modifiers=[Key.cmd])
            self.ca.tap(Key.esc)

        return _new_window()

    def close_window(self):
        @self.ca.register
        def _close_window():
            self.ca.tap("w", modifiers=[Key.cmd, Key.shift])

        return _close_window()

    def refresh(self):
        @self.ca.register
        def _refresh():
            self.ca.tap("r", modifiers=[Key.cmd])

        return _refresh()

    def toggle_devtools(self):
        @self.ca.register
        def _toggle_devtools():
            self.ca.tap("i", modifiers=[Key.cmd, Key.alt])

        return _toggle_devtools()

    def prev_devtools_panel(self, times: int = 1):
        @self.ca.register
        def _prev_devtools_panel():
            for _ in range(times):
                self.ca.tap("[", modifiers=[Key.cmd])

        return _prev_devtools_panel()

    def next_devtools_panel(self, times: int = 1):
        @self.ca.register
        def _next_devtools_panel():
            for _ in range(times):
                self.ca.tap("]", modifiers=[Key.cmd])

        return _next_devtools_panel()
