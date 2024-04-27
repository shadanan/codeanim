import time
from typing import Callable, Concatenate, ParamSpec, TypeVar

import pyperclip
from pynput.keyboard import Key
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

        self.backspace = backspace
        self.click = click
        self.drag = drag
        self.move = move
        self.paste = paste
        self.tap = tap
        self.wait = self.keyboard.wait
        self.write = write

        self._call_stack = []

    def __enter__(self):
        self.start()
        return self

    def start(self):
        self.keyboard.start()

    def __exit__(self, *args):
        self.stop()

    def stop(self):
        self.keyboard.stop()

    @staticmethod
    def cmd(func: Callable[Concatenate["CodeAnim", P], R]) -> Callable[P, R]:
        def codeanim_func(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> R:
            codeanim._call_stack.append(func.__name__)
            result = func(codeanim, *args, **kwargs)
            codeanim._call_stack.pop()
            if len(codeanim._call_stack) == 0:
                codeanim.delay.pause()
            return result

        return codeanim_func


@CodeAnim.cmd
def backspace(ca: CodeAnim, num: int = 1):
    for _ in range(num):
        ca.tap(Key.backspace)


@CodeAnim.cmd
def click(
    ca: CodeAnim,
    pos: tuple[int, int] | None = None,
    button: Button = Button.left,
    count: int = 1,
    *,
    start: tuple[int, int] | None = None,
    interpolator: Interpolator = Spring(),
):
    if pos is not None:
        move(pos, start=start, interpolator=interpolator)
    ca.mouse.click(button, count)


@CodeAnim.cmd
def drag(
    ca: CodeAnim,
    start: tuple[int, int],
    end: tuple[int, int],
    button: Button = Button.left,
    *,
    interpolator: Interpolator = Spring(),
):
    move(start, interpolator=interpolator)
    ca.mouse.press(button)
    move(end, interpolator=interpolator)
    ca.mouse.release(button)


@CodeAnim.cmd
def move(
    ca: CodeAnim,
    end: tuple[int, int],
    *,
    start: tuple[int, int] | None = None,
    steps: int = 1000,
    step_size: float = 0.01,
    delay: float = 0.01,
    interpolator: Interpolator = Spring(),
):
    if start is None:
        start = ca.mouse.position

    delta = end[0] - start[0], end[1] - start[1]

    for step in range(steps):
        pt, vt = interpolator(step * step_size)
        if done(pt, vt):
            break
        ca.mouse.position = int(start[0] + delta[0] * pt), int(start[1] + delta[1] * pt)
        time.sleep(delay)
    ca.mouse.position = end


@CodeAnim.cmd
def paste(ca: CodeAnim, text: str, *, paste_delay: float = 0.5):
    pyperclip.copy(text)
    ca.tap("v", modifiers=[Key.cmd])
    time.sleep(paste_delay)  # Need to wait for the paste to finish


@CodeAnim.cmd
def tap(ca: CodeAnim, key: str | Key, *, modifiers: list[Key] = [], repeat: int = 1):
    for modifier in modifiers:
        ca.keyboard.controller.press(modifier)
    for _ in range(repeat):
        ca.keyboard.controller.tap(key)
        time.sleep(ca.delay.keys.get(key, ca.delay.tap))
    for modifier in modifiers:
        ca.keyboard.controller.release(modifier)


@CodeAnim.cmd
def write(ca: CodeAnim, text: str):
    for char in text:
        if char == "\n":
            ca.tap(Key.enter)
        elif char == "\t":
            ca.tap(Key.tab)
        elif len(char.encode("utf-8")) != 1:
            ca.paste(char)
        else:
            ca.tap(char)


def done(position: float, velocity: float) -> bool:
    return abs(1 - position) < 0.001 and velocity < 0.01


codeanim = CodeAnim()
