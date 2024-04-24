import time
from threading import Event

from pynput.keyboard import Controller, Key, KeyCode, Listener


class Keyboard:
    def __init__(self):
        self.keyboard = Controller()
        self.press = Event()
        self.released: Key | KeyCode | None = None
        self.listener: Listener | None = None

    def handle_press(self, key: Key | KeyCode | None):
        pass

    def handle_release(self, key: Key | KeyCode | None):
        self.released = key
        self.press.set()

    def __enter__(self):
        self.start()
        return self

    def start(self):
        self.listener = Listener(
            on_press=self.handle_press,
            on_release=self.handle_release,
        )
        self.listener.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def stop(self):
        if self.listener is not None:
            self.listener.stop()
            self.listener.join()
            self.listener = None

    def tap(
        self,
        key: str | Key,
        *,
        modifiers: list[Key] = [],
        repeat: int = 1,
        delay: float = 0,
    ):
        for modifier in modifiers:
            self.keyboard.press(modifier)
        for _ in range(repeat):
            self.keyboard.tap(key)
            time.sleep(delay)
        for modifier in modifiers:
            self.keyboard.release(modifier)

    def wait(self, key: Key = Key.shift):
        if self.listener is None or not self.listener.is_alive():
            raise RuntimeError("KeyMonitor is not running.")
        time.sleep(0.01)  # Flush previous tap events
        self.released = None
        print(f"Tap {key.name} to continue")
        while key != self.released:
            self.press.wait()
            self.press.clear()
