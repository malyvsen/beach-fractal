import numpy as np
from PIL import ImageOps
from stqdm import stqdm
from .beach import Beach
from .grain import Grain, FreeGrain, TakenGrain


def from_image(image):
    are_taken = np.array(ImageOps.grayscale(image)).T < 127
    assert len(are_taken.shape) == 2

    def is_edge(x, y):
        if not are_taken[x, y]:
            return False
        if x > 0 and not are_taken[x - 1, y]:
            return True
        if x + 1 < are_taken.shape[0] and not are_taken[x + 1, y]:
            return True
        if y > 0 and not are_taken[x, y - 1]:
            return True
        if y + 1 < are_taken.shape[1] and not are_taken[x, y + 1]:
            return True
        return False

    edge_coords = [
        (x, y)
        for x in range(are_taken.shape[0])
        for y in range(are_taken.shape[1])
        if is_edge(x, y)
    ]
    grains = {}
    for x, column in enumerate(stqdm(are_taken, desc="Indexing image")):
        for y, is_taken in enumerate(column):
            if is_taken:
                grains[(x, y)] = TakenGrain(taken_radius=0)
            else:
                grains[(x, y)] = FreeGrain(
                    free_radius=min(
                        Grain.distance((x, y), edge_coord) for edge_coord in edge_coords
                    )
                )
    return Beach(grains=grains)


Beach.from_image = from_image
