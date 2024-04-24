import math
import time
from dataclasses import dataclass
from typing import Generator, Protocol

Point = tuple[int, int]


class Interpolator(Protocol):
    def interpolate(self, t: float) -> float: ...
    def __call__(self, start: Point, end: Point) -> Generator[Point, None, None]: ...


@dataclass
class Sigmoid(Interpolator):
    steps: int = 100
    delay: float = 0.01
    speed: float = 10

    def interpolate(self, t: float) -> float:
        return 1 / (1 + math.exp((0.5 - t) * self.speed))

    def __call__(self, start: Point, end: Point) -> Generator[Point, None, None]:
        dx, dy = end[0] - start[0], end[1] - start[1]
        for step in range(self.steps):
            ft = self.interpolate(step / self.steps)
            yield (int(start[0] + dx * ft), int(start[1] + dy * ft))
            time.sleep(self.delay)
        yield end


@dataclass
class Spring(Interpolator):
    mass: float = 1
    stiffness: float = 1
    damping: float = 2
    speed: float = 10
    steps: int = 100
    delay: float = 0.01

    def __post_init__(self):
        self.omega = math.sqrt(self.stiffness / self.mass)
        self.zeta = self.damping / (2 * math.sqrt(self.stiffness * self.mass))

    def interpolate(self, t: float) -> float:
        return 1 - math.exp(-self.zeta * self.omega * t * self.speed) * math.cos(
            self.omega * math.sqrt(1 - self.zeta**2) * t * self.speed
        )

    def __call__(self, start: Point, end: Point) -> Generator[Point, None, None]:
        dx, dy = end[0] - start[0], end[1] - start[1]
        for step in range(self.steps):
            ft = self.interpolate(step / self.steps)
            yield (int(start[0] + dx * ft), int(start[1] + dy * ft))
            time.sleep(self.delay)
        yield end
