import math
import time

from pynput.mouse import Button

from .core import CodeAnim
from .interpolators import Interpolator, Spring

Point = tuple[int, int]


def is_within_epsilon(p1: Point, p2: Point) -> bool:
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2) < 2


@CodeAnim.cmd
def move(
    ca: CodeAnim,
    end: Point,
    *,
    start: Point | None = None,
    steps: int = 100,
    delay: float = 0.01,
    interpolator: Interpolator = Spring(),
):
    if start is None:
        start = ca.mouse.position

    delta = end[0] - start[0], end[1] - start[1]
    for step in range(steps):
        ft = interpolator(step / steps)
        pos = int(start[0] + delta[0] * ft), int(start[1] + delta[1] * ft)
        if is_within_epsilon(pos, end):
            break
        ca.mouse.position = pos
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
