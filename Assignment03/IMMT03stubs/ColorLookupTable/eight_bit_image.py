"""Assignment 03: simple RGB332 quantization and reconstruction."""

import argparse
from pathlib import Path

import numpy
import numpy as np

from image_io import read_image, write_image

BASE_DIR = Path(__file__).resolve().parent
RED_BITS = 3
GREEN_BITS = 3
BLUE_BITS = 2


def create_8bit_image(image: np.ndarray) -> np.ndarray:
    """Return uint8 codes of shape (height, width), with bit layout RRRGGGBB.

    TODO: keep the 3 most significant bits of R/G and the 2 most significant
    bits of B, then pack them into one byte per pixel using bit operations.
    Do not change the input RGB image.
    """
    eight_bit_image = np.zeros(image.shape[:2], dtype=np.uint8)

    for y, row in enumerate(image):
        for x, pixel in enumerate(row):
            r = pixel[0] & 0b11100000
            g = (pixel[1] & 0b11100000) >> 3
            b = (pixel[2] & 0b11000000) >> 6
            single = r | g | b
            eight_bit_image[y, x] = single

    return eight_bit_image


def reconstruct(data: np.ndarray) -> np.ndarray:
    """Return a new uint8 RGB image, shape (height, width, 3).

    TODO: unpack RRRGGGBB. Scale each R/G code c to c*255/7 and each B code
    c to c*255/3; round with floor(value + 0.5). Use wider/float arithmetic.
    Do not interpret these color codes as grayscale intensities.
    """
    image = []

    for y, row in enumerate(data):
        image.append([])
        for x, pixel in enumerate(row):
            r = int(pixel & 0b11100000) >> 5
            g = int(pixel & 0b00011100) >> 2
            b = int(pixel & 0b00000011)

            r = r * 255 / 7
            g = g * 255 / 7
            b = b * 255 / 3

            r = np.uint8(r+0.5)
            g = np.uint8(g+0.5)
            b = np.uint8(b+0.5)

            color = numpy.array([r, g, b], dtype=np.uint8)
            image[y].append(color)

    return np.array(image, dtype=np.uint8)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=BASE_DIR / "mandrill_512x512.png")
    parser.add_argument("--output", type=Path,
                        default=BASE_DIR / "mandrill_512x512_reconstructed_8bpp.png")
    args = parser.parse_args()
    image = read_image(args.input)
    codes = create_8bit_image(image)
    result = reconstruct(codes)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_image(result, args.output)
    print(f"Saved RGB reconstruction to {args.output}")


if __name__ == "__main__":
    main()
