from pynput.mouse import Button

from .core import CodeAnim
from .interpolators import Interpolator, Point, Spring


@CodeAnim.cmd
def move(
    ca: CodeAnim,
    end: Point,
    *,
    start: Point | None = None,
    interpolator: Interpolator = Spring(),
):
    if start is None:
        start = ca.mouse.position
    for pos in interpolator(start, end):
        ca.mouse.position = pos


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
    print(button)
    ca.mouse.click(button, count)
