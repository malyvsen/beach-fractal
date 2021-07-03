import numpy as np
from PIL import ImageOps
from .beach import Beach
from .point import FreePoint, TakenPoint


def from_image(image):
    array = np.array(ImageOps.grayscale(image))
    assert len(array.shape) == 2
    free = set()
    taken = set()
    for y, row in enumerate(array):
        for x, pixel in enumerate(row):
            if pixel < 127:
                taken.add(TakenPoint(x=x, y=y, taken_step=0, distance=0))
            else:
                free.add(FreePoint(x=x, y=y))
    return Beach(free=free, taken=taken)


Beach.from_image = from_image
