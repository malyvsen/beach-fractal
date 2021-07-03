from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def distance(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2


@dataclass(frozen=True)
class FreePoint:
    pass


@dataclass(frozen=True)
class TakenPoint:
    taken_step: int
    distance: float
