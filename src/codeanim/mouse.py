import time

from pynput.mouse import Button

from .core import CodeAnim
from .interpolators import Interpolator, Spring

Point = tuple[int, int]


def done(position: float, velocity: float) -> bool:
    return abs(1 - position) < 0.001 and velocity < 0.01


@CodeAnim.cmd
def move(
    ca: CodeAnim,
    end: Point,
    *,
    start: Point | None = None,
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
def click(
    ca: CodeAnim,
    pos: Point | None = None,
    button: Button = Button.left,
    count: int = 1,
    *,
    start: Point | None = None,
    interpolator: Interpolator = Spring(),
):
    if pos is not None:
        move(pos, start=start, interpolator=interpolator)
    ca.mouse.click(button, count)


@CodeAnim.cmd
def drag(
    ca: CodeAnim,
    start: Point,
    end: Point,
    button: Button = Button.left,
    *,
    interpolator: Interpolator = Spring(),
):
    move(start, interpolator=interpolator)
    ca.mouse.press(button)
    move(end, interpolator=interpolator)
    ca.mouse.release(button)
