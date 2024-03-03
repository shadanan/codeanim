import time
from contextlib import contextmanager
from dataclasses import dataclass, field

from pynput.keyboard import Key


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
