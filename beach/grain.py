from dataclasses import dataclass


@dataclass(frozen=True)
class Grain:
    @staticmethod
    def distance(coords1, coords2):
        return ((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2) ** 0.5


@dataclass(frozen=True)
class FreeGrain(Grain):
    free_radius: float


@dataclass(frozen=True)
class TakenGrain(Grain):
    taken_radius: float
