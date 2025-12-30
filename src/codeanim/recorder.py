from dataclasses import dataclass, field
from time import sleep
from typing import Any, TypeGuard

from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode


def is_key(key: Any) -> TypeGuard[Key]:
    return isinstance(key, Key)


def is_key_code(key: Any) -> TypeGuard[KeyCode]:
    return isinstance(key, KeyCode)


@dataclass
class Recorder:
    abort_key: Key | KeyCode
    verbose: bool
    mouse_listener: mouse.Listener | None = None
    keyboard_listener: keyboard.Listener | None = None
    mouse_event: tuple[int, int] | None = None

    keys: set[Key] = field(default_factory=set[Key])

    def handle_press(self, key: Key | KeyCode | None):
        if self.verbose:
            print("press", key, type(key), is_key(key), is_key_code(key))

        if key == self.abort_key:
            if self.keyboard_listener is not None:
                self.keyboard_listener.stop()
            if self.mouse_listener is not None:
                self.mouse_listener.stop()

        if is_key(key):
            self.keys.add(key)

    def handle_release(self, key: Key | KeyCode | None):
        if self.verbose:
            print("release", key, type(key), is_key(key), is_key_code(key))

        if is_key(key):
            print(f"tap({key})")
            self.keys.remove(key)

        if is_key_code(key) and key.char is not None:
            args = [f'"{key.char}"']
            if self.keys:
                args.append(f"modifiers=[{', '.join(map(str, self.keys))}]")
            print(f"tap({', '.join(args)})")

    def handle_down(self, x: int, y: int, button: mouse.Button):
        if self.verbose:
            print("down", x, y, button)
        self.mouse_event = (x, y)

    def handle_up(self, x: int, y: int, button: mouse.Button):
        if self.verbose:
            print("up", x, y, button)
        if self.mouse_event is not None:
            prev_x, prev_y = self.mouse_event
            args = [f"({x}, {y})"]
            if button != mouse.Button.left:
                args.append(f"{button}")
            if x == prev_x and y == prev_y:
                func = "click"
            else:
                func = "drag"
                args.insert(0, f"({prev_x}, {prev_y})")
            print(f"{func}({', '.join(args)})")

    def handle_click(self, x: float, y: float, button: mouse.Button, down: bool):
        if down:
            self.handle_down(int(x), int(y), button)
        else:
            self.handle_up(int(x), int(y), button)

    def __enter__(self):
        self.start()
        return self

    def start(self):
        self.mouse_listener = mouse.Listener(on_click=self.handle_click)
        self.mouse_listener.start()
        sleep(0.01)

        self.keyboard_listener = keyboard.Listener(
            on_press=self.handle_press, on_release=self.handle_release
        )
        self.keyboard_listener.start()
        sleep(0.01)

    def __exit__(self, *args: tuple[Any]):
        self.stop()

    def stop(self):
        if self.keyboard_listener is not None:
            self.keyboard_listener.stop()
            self.keyboard_listener.join()
            self.keyboard_listener = None

        if self.mouse_listener is not None:
            self.mouse_listener.stop()
            self.mouse_listener.join()
            self.mouse_listener = None

    def wait(self):
        if self.keyboard_listener is None or self.mouse_listener is None:
            raise RuntimeError("Recorder is not running.")

        print(f"Recording mouse and keyboard inputs. Press {self.abort_key} to quit.")
        self.keyboard_listener.join()
        self.mouse_listener.join()
