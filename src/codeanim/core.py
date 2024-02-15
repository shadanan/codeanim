import subprocess
import time
from contextlib import contextmanager
from dataclasses import dataclass, field

import pyperclip
from pynput.keyboard import Controller, Key

keyboard = Controller()


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


delayer = Delayer()


def set_delays(
    *,
    tap: float | None = None,
    keys: dict[str | Key, float] | None = None,
    end: float | None = None,
):
    prev_tap, delayer.tap = delayer.tap, delayer.tap if tap is None else tap
    prev_keys, delayer.keys = delayer.keys, delayer.keys if keys is None else keys
    prev_end, delayer.end = delayer.end, delayer.end if end is None else end
    return prev_tap, prev_keys, prev_end


@contextmanager
def delays(
    *,
    tap: float | None = None,
    keys: dict[str | Key, float] | None = None,
    end: float | None = None,
):
    prev_tap, prev_keys, prev_end = set_delays(tap=tap, keys=keys, end=end)
    yield
    delayer.tap, delayer.keys, delayer.end = prev_tap, prev_keys, prev_end


def no_delays():
    return delays(tap=0, keys={}, end=0)


def no_final_delay():
    return delays(end=0)


def delay(end: float | None = None):
    end = delayer.end if end is None else end
    time.sleep(end)


def codeanim(func):
    def codeanim_func(*args, **kwargs):
        func(*args, **kwargs)
        delay()

    return codeanim_func


def tap(key: str | Key, *, modifiers: list[str | Key] = []):
    for modifier in modifiers:
        keyboard.press(modifier)
    keyboard.tap(key)
    for modifier in modifiers:
        keyboard.release(modifier)
    time.sleep(delayer.keys.get(key, delayer.tap))


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
