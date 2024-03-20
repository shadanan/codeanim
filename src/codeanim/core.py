import time
from typing import Callable, Concatenate, ParamSpec, TypeVar

import pyperclip
from pynput.keyboard import Key

from . import shell
from .delayer import Delayer
from .keyboard import Keyboard

R = TypeVar("R")
P = ParamSpec("P")


class CodeAnim:
    def __init__(self):
        self.delay = Delayer()
        self.keyboard = Keyboard()
        self.backspace = backspace
        self.write = write
        self.shell = shell
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

    def tap(self, key: str | Key, *, modifiers: list[str | Key] = [], repeat: int = 1):
        self.keyboard.tap(
            key,
            modifiers=modifiers,
            repeat=repeat,
            delay=self.delay.keys.get(key, self.delay.tap),
        )

    def wait(self, key: Key = Key.shift):
        self.keyboard.wait(key)

    def paste(self, text: str, *, paste_delay: float = 0.5):
        pyperclip.copy(text)
        self.tap("v", modifiers=[Key.cmd])
        time.sleep(paste_delay)  # Need to wait for the paste to finish


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


@CodeAnim.cmd
def backspace(ca: CodeAnim, num: int = 1):
    for _ in range(num):
        ca.tap(Key.backspace)


codeanim = CodeAnim()
