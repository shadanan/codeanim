import time
from typing import Any, Callable, ParamSpec, TypeVar

import pyperclip
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button, Controller

from . import shell
from .delayer import Delayer
from .interpolators import Interpolator, Spring
from .keyboard import Keyboard

R = TypeVar("R")
P = ParamSpec("P")


class CodeAnim:
    def __init__(self):
        self.delay = Delayer()
        self.keyboard = Keyboard()
        self.mouse = Controller()
        self.shell = shell
        self._call_stack: list[str] = []
        self.pause = self.delay.pause
        self.wait = self.keyboard.wait

    def __enter__(self):
        self.start()
        return self

    def start(self):
        self.keyboard.start()

    def __exit__(self, *args: tuple[Any]):
        self.stop()

    def stop(self):
        self.keyboard.stop()

    def register(self, func: Callable[P, R]) -> Callable[P, R]:
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> R:
            if self.keyboard.aborted:
                raise Exception("aborted")
            self._call_stack.append(func.__name__)
            result = func(*args, **kwargs)
            self._call_stack.pop()
            if len(self._call_stack) == 0:
                self.delay.pause()
            return result

        return wrapper

    def backspace(self, num: int = 1):
        @self.register
        def _backspace():
            for _ in range(num):
                self.tap(Key.backspace)

        return _backspace()

    def click(
        self,
        pos: tuple[int, int] | None = None,
        button: Button = Button.left,
        count: int = 1,
        *,
        start: tuple[int, int] | None = None,
        interpolator: Interpolator = Spring(),
    ):
        @self.register
        def _click():
            if pos is not None:
                self.move(pos, start=start, interpolator=interpolator)
            self.mouse.click(button, count)

        return _click()

    def drag(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        button: Button = Button.left,
        *,
        interpolator: Interpolator = Spring(),
    ):
        @self.register
        def _drag():
            self.move(start, interpolator=interpolator)
            self.mouse.press(button)
            self.move(end, interpolator=interpolator)
            self.mouse.release(button)

        return _drag()

    def move(
        self,
        end: tuple[int, int],
        *,
        start: tuple[int, int] | None = None,
        steps: int = 1000,
        step_size: float = 0.01,
        delay: float = 0.01,
        interpolator: Interpolator = Spring(),
    ):
        @self.register
        def _move():
            nonlocal start
            if start is None:
                start = self.mouse.position

            delta = end[0] - start[0], end[1] - start[1]

            for step in range(steps):
                pt, vt = interpolator(step * step_size)
                if abs(1 - pt) < 0.001 and vt < 0.01:
                    break
                self.mouse.position = (
                    round(start[0] + delta[0] * pt),
                    round(start[1] + delta[1] * pt),
                )
                time.sleep(delay)
            self.mouse.position = end

        return _move()

    def paste(self, text: str, *, paste_delay: float = 0.5):
        @self.register
        def _paste():
            pyperclip.copy(text)
            self.tap("v", modifiers=[Key.cmd])
            time.sleep(paste_delay)  # Need to wait for the paste to finish

        return _paste()

    def scroll(self, dx: int, dy: int):
        @self.register
        def _scroll():
            self.mouse.scroll(dx, dy)

        return _scroll()

    def tap(
        self,
        key: str | Key | KeyCode,
        *,
        modifiers: list[Key] = [],
        repeat: int = 1,
    ):
        @self.register
        def _tap():
            for modifier in modifiers:
                self.keyboard.controller.press(modifier)
            for _ in range(repeat):
                self.keyboard.controller.tap(key)
                time.sleep(self.delay.keys.get(key, self.delay.tap))
            for modifier in modifiers:
                self.keyboard.controller.release(modifier)

        return _tap()

    def write(self, text: str):
        @self.register
        def _write():
            for char in text:
                if char == "\n":
                    self.tap(Key.enter)
                elif char == "\t":
                    self.tap(Key.tab)
                elif char == "\b":
                    self.tap(Key.backspace)
                elif len(char.encode("utf-8")) != 1:
                    self.paste(char)
                else:
                    self.tap(char)

        return _write()
