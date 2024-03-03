import os
import subprocess


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
