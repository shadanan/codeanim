import math
from dataclasses import dataclass
from typing import Protocol


class Interpolator(Protocol):
    def __call__(self, t: float) -> float: ...


@dataclass
class Sigmoid(Interpolator):
    scale: float = 10

    def __call__(self, t: float) -> float:
        return 1 / (1 + math.exp((0.5 - t) * self.scale))


@dataclass
class Spring(Interpolator):
    mass: float = 1
    stiffness: float = 1
    damping: float = 2
    scale: float = 10

    def __post_init__(self):
        self.omega = math.sqrt(self.stiffness / self.mass)
        self.zeta = self.damping / (2 * math.sqrt(self.stiffness * self.mass))

    def __call__(self, t: float) -> float:
        return 1 - math.exp(-self.zeta * self.omega * t * self.scale) * math.cos(
            self.omega * math.sqrt(1 - self.zeta**2) * t * self.scale
        )
