from threading import Event

from pynput.keyboard import Key, KeyCode, Listener


class KeyMonitor:
    def __init__(self):
        self.press = Event()
        self.released: Key | KeyCode | None = None

    def handle_release(self, key: Key | KeyCode | None):
        self.released = key
        self.press.set()

    def start(self):
        self.listener = Listener(on_release=self.handle_release)
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def wait(self, key: Key):
        print(f"Press and release {key.name} to continue")
        while key != self.released:
            self.press.wait()
            self.press.clear()


monitor = KeyMonitor()
monitor.start()


def wait(key: Key = Key.shift):
    monitor.wait(key)
