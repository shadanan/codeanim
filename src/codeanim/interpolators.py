import math
from dataclasses import dataclass
from typing import Protocol


class Interpolator(Protocol):
    def __call__(self, t: float) -> tuple[float, float]: ...


@dataclass
class Sigmoid(Interpolator):
    speed: float = 4
    offset: float = 8

    def __call__(self, t: float) -> tuple[float, float]:
        exp = math.exp(self.offset - t * self.speed**2)
        return 1 / (1 + exp), abs(exp / (1 + exp**2))


@dataclass
class Spring(Interpolator):
    gamma: float = 10
    omega: float = 0

    def __call__(self, t: float) -> tuple[float, float]:
        exp = math.exp(-self.gamma * t)
        cos, sin = math.cos(self.omega * t), math.sin(self.omega * t)
        return 1 - exp * cos, abs(exp * (self.gamma * cos + self.omega * sin))
