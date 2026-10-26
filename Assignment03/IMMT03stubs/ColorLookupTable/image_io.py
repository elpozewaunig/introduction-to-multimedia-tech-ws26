"""Image I/O to complete; reuse your grayscale I/O with RGB mode."""

from pathlib import Path

import numpy as np
from PIL import Image


def read_image(path: str | Path) -> np.ndarray:
    """Return a writable uint8 RGB array, shape (height, width, 3).

    TODO: open with Pillow, convert explicitly to 'RGB', create an independent
    NumPy array, and close the Pillow image (e.g. with a context manager).
    """
    with Image.open(path).convert("RGB") as image:
        return np.array(image)


def write_image(image: np.ndarray, path: str | Path) -> None:
    """TODO: save the supplied uint8 RGB array as a PNG using Pillow."""
    img = Image.fromarray(image)
    img.save(path)
    img.close()
