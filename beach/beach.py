from typing import Set
from dataclasses import dataclass
from functools import cached_property
import numpy as np
from PIL import Image
from stqdm import stqdm
from .point import FreePoint, TakenPoint


@dataclass(frozen=True)
class Beach:
    free: Set[FreePoint]
    taken: Set[TakenPoint]

    @property
    def next(self):
        point = None
        distance = None
        for candidate in stqdm(self.free, desc="Deciding next step"):
            candidate_distance = min(candidate.distance(taken) for taken in self.taken)
            if point is None or candidate_distance > distance:
                point = candidate
                distance = candidate_distance
        return type(self)(
            free=self.free - {point},
            taken=Set.union(
                self.taken,
                {
                    TakenPoint(
                        x=point.x,
                        y=point.y,
                        taken_step=len(self.taken),
                        distance=distance,
                    )
                },
            ),
        )

    @cached_property
    def span(self):
        return (
            (self.extreme(min, "x"), self.extreme(max, "x")),
            (self.extreme(min, "y"), self.extreme(max, "y")),
        )

    def render(self, attribute):
        if len(self.taken) == 0:
            brightness = lambda point: 0
        else:
            getter = lambda point: getattr(point, attribute)
            attributes = lambda: map(getter, self.taken)
            min_attr = min(attributes())
            max_attr = max(attributes())
            if min_attr == max_attr:
                brightness = lambda point: 0
            else:
                brightness = lambda point: (getter(point) - min_attr) / (
                    max_attr - min_attr
                )
        array = np.zeros(
            (
                self.span[1][1] - self.span[1][0] + 1,
                self.span[0][1] - self.span[0][0] + 1,
            )
        )
        for taken in self.taken:
            array[taken.y - self.span[1][0], taken.x - self.span[0][0]] = brightness(
                taken
            )
        return Image.fromarray(np.round(array * 255).astype(np.uint8))

    def extreme(self, side, attribute):
        point = side(
            self.free | self.taken, key=lambda point: getattr(point, attribute)
        )
        return getattr(point, attribute)
