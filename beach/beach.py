from typing import Set
from dataclasses import dataclass
from functools import cached_property
import numpy as np
from PIL import Image
from .point import FreePoint, TakenPoint


@dataclass(frozen=True)
class Beach:
    free: Set[FreePoint]
    taken: Set[TakenPoint]

    @property
    def next(self):
        point, distance = max(
            (
                (free, min(self.taken, lambda taken: free.distance(taken)))
                for free in self.free
            ),
            key=lambda pair: pair[1],
        )
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
        getter = lambda point: getattr(point, attribute)
        attributes = map(getter, self.taken)
        min_attr = min(attributes)
        max_attr = max(attributes)
        brightness = lambda point: (getter(point) - min_attr) / (max_attr - min_attr)
        array = np.zeros(
            self.span[1][1] - self.span[1][0] + 1, self.span[0][1] - self.span[0][0] + 1
        )
        for taken in self.taken:
            array[taken.y - self.span[1][0], taken.x - self.span[0][0]] = brightness(
                taken
            )
        return Image.fromarray(array)

    def extreme(self, side, attribute):
        point = side(self.free | self.taken, key=lambda point: getattr(attribute))
        return getattr(point, attribute)
