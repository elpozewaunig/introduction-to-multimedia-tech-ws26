"""Assignment 03: simple RGB332 quantization and reconstruction."""

import argparse
from pathlib import Path

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
    raise NotImplementedError("Implement create_8bit_image")


def reconstruct(data: np.ndarray) -> np.ndarray:
    """Return a new uint8 RGB image, shape (height, width, 3).

    TODO: unpack RRRGGGBB. Scale each R/G code c to c*255/7 and each B code
    c to c*255/3; round with floor(value + 0.5). Use wider/float arithmetic.
    Do not interpret these color codes as grayscale intensities.
    """
    raise NotImplementedError("Implement reconstruct")


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
