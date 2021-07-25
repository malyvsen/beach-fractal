from typing import Dict, Tuple
from dataclasses import dataclass, replace
import math
import numpy as np
from PIL import Image
from .grain import Grain, FreeGrain, TakenGrain


@dataclass(frozen=True)
class Beach:
    grains: Dict[Tuple[int, int], Grain]

    @property
    def free(self):
        return [grain for grain in self.grains.values() if isinstance(grain, FreeGrain)]

    @property
    def next(self):
        coords = max(
            (
                coords
                for coords in self.grains.keys()
                if isinstance(self.grains[coords], FreeGrain)
            ),
            key=lambda coords: self.grains[coords].free_radius,
        )
        grain = self.grains[coords]
        result = self.grains.copy()
        result[coords] = TakenGrain(taken_radius=grain.free_radius)
        make_range = lambda coord_id: range(
            math.floor(coords[coord_id] - grain.free_radius + 1),
            math.ceil(coords[coord_id] + grain.free_radius),
        )
        for x in make_range(0):
            for y in make_range(1):
                if isinstance(result[(x, y)], TakenGrain):
                    continue
                distance = Grain.distance(coords, (x, y))
                result[(x, y)] = replace(
                    result[(x, y)],
                    free_radius=min(result[(x, y)].free_radius, distance),
                )
        return type(self)(grains=result)

    def render(self):
        span = (
            lambda coord_id: max(coords[coord_id] for coords in self.grains.keys()) + 1
        )
        array = np.zeros((span(0), span(1)))
        for coords, grain in self.grains.items():
            if isinstance(grain, FreeGrain):
                continue
            array[coords[0], coords[1]] = grain.taken_radius
        if array.max() > 0:
            array /= array.max()
        return Image.fromarray(np.round(array * 255).astype(np.uint8).T)
