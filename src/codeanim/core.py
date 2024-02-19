import os
import subprocess
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Callable, ParamSpec, TypeVar

import pyperclip
from pynput.keyboard import Controller, Key

keyboard = Controller()


def expand(path: str) -> str:
    return os.path.expandvars(os.path.expanduser(path))


def open(path: str):
    path = expand(path)
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist")
    return subprocess.check_output(["open", path])


def code(path: str):
    path = expand(path)
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist")
    return subprocess.check_output(["code", path])


def osascript(cmd: str) -> str:
    return subprocess.check_output(["osascript", "-e", cmd]).decode().strip()


def activate(app_name: str):
    osascript(f'tell application "{app_name}" to activate')


def resize(process_name: str, position: tuple[int, int], size: tuple[int, int]):
    osascript(
        f"""
        tell application "System Events" to tell process "{process_name}"
          tell front window
            set position to {{{position[0]}, {position[1]}}}
            set size to {{{size[0]}, {size[1]}}}
          end tell
        end tell
        """
    )


@dataclass
class Delayer:
    tap: float = 0.02
    keys: dict[str | Key, float] = field(default_factory=dict)
    end: float = 1

    def set(
        self,
        end: float | None = None,
        *,
        tap: float | None = None,
        keys: dict[str | Key, float] | None = None,
    ):
        prev_end, self.end = self.end, self.end if end is None else end
        prev_tap, self.tap = self.tap, self.tap if tap is None else tap
        prev_keys, self.keys = self.keys, self.keys if keys is None else keys
        return prev_end, prev_tap, prev_keys

    def pause(self, end: float | None = None):
        end = self.end if end is None else end
        time.sleep(end)

    @contextmanager
    def __call__(
        self,
        end: float | None = None,
        *,
        tap: float | None = None,
        keys: dict[str | Key, float] | None = None,
    ):
        prev_end, prev_tap, prev_keys = self.set(end=end, tap=tap, keys=keys)
        yield
        self.set(end=prev_end, tap=prev_tap, keys=prev_keys)


delay = Delayer()


R = TypeVar("R")
P = ParamSpec("P")


def codeanim(func: Callable[P, R]) -> Callable[P, R]:
    def codeanim_func(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        result = func(*args, **kwargs)
        delay.pause()
        return result

    return codeanim_func


def tap(key: str | Key, *, modifiers: list[str | Key] = []):
    for modifier in modifiers:
        keyboard.press(modifier)
    keyboard.tap(key)
    for modifier in modifiers:
        keyboard.release(modifier)
    time.sleep(delay.keys.get(key, delay.tap))


@codeanim
def paste(text: str, *, paste_delay: float = 0.5):
    pyperclip.copy(text)
    tap("v", modifiers=[Key.cmd])
    time.sleep(paste_delay)  # Need to wait for the paste to finish


@codeanim
def write(text: str):
    for char in text:
        if char == "\n":
            tap(Key.enter)
        elif char == "\t":
            tap(Key.tab)
        elif len(char.encode("utf-8")) != 1:
            paste(char)
        else:
            tap(char)


@codeanim
def backspace(num: int = 1):
    for _ in range(num):
        tap(Key.backspace)
