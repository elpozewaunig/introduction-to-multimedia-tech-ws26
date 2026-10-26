"""Assignment 03: complete the TODO functions; the CLI is provided."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

from histogram import plot_histogram, plot_images

BASE_DIR = Path(__file__).resolve().parent


def open_image(path: str | Path) -> np.ndarray:
    """Return a writable uint8 grayscale array, shape (height, width).

    TODO: open with Pillow, explicitly convert to mode 'L', and create an
    independent NumPy array. The supplied PNG is stored as RGB.
    Close the Pillow image after loading, e.g. with a context manager.
    """
    with Image.open(path).convert("L") as image:
        print(np.array(image, dtype=np.uint8))
        return np.array(image)


def calc_histogram(image: np.ndarray) -> np.ndarray:
    """Return 256 integer counts (dtype int64), one for each gray value.

    TODO: count all pixels yourself. The sum must equal image.size.
    """
    histogram = np.zeros((256,), dtype=np.int64)

    for row in image:
        for pixel in row:
            histogram[pixel] += 1

    print(histogram)
    return histogram


def calc_lower_bound(hist: np.ndarray, d: float) -> int:
    """Return the first bin from the low end whose cumulative count > floor(d*N).

    TODO: N = sum(hist); d is a fraction at each end, 0 <= d < 0.5.
    For d=0, return the smallest occupied gray value. Hist is nonempty.
    """
    total_pixels = np.sum(hist)
    d_bound = total_pixels * d

    pixels_encountered = 0
    for bin_index, bin_count in enumerate(hist):
        pixels_encountered += bin_count
        if pixels_encountered >= d_bound:
            return bin_index
    return 255


def calc_upper_bound(hist: np.ndarray, d: float) -> int:
    """Return the first bin from the high end whose cumulative count > floor(d*N).

    TODO: use the same convention as calc_lower_bound, scanning in reverse.
    For d=0, return the largest occupied gray value.
    """
    total_pixels = np.sum(hist)
    d_bound = total_pixels * d

    pixels_encountered = 0
    hist = np.flip(hist) #reverses the array
    for bin_index, bin_count in enumerate(hist):
        pixels_encountered += bin_count
        if pixels_encountered >= d_bound:
            return 255 - bin_index
    return 0


def stretch_histogram(image: np.ndarray, low: int, high: int) -> np.ndarray:
    """Return a new uint8 image; do not change the input.

    TODO: linearly map [low, high] to [0, 255]. Calculate in a wider/float
    type, clip to [0, 255], round with floor(value + 0.5), then use uint8.
    The equal-bound case is already handled below.
    """
    if low == high:
        return image.copy()

    new_image = image.copy()
    for y, row in enumerate(image):
        for x, pix in enumerate(row):
            value = ((pix - low) / (high - low)) * 255
            value = np.uint8(value + 0.5) # Round
            value = np.clip(value, 0, 255, dtype = np.uint8) # Clip
            new_image[y][x] = value

    return new_image


def write_image(image: np.ndarray, path: str | Path) -> None:
    """TODO: save the supplied uint8 grayscale array as a PNG using Pillow."""
    img = Image.fromarray(image)
    img.save(path)
    img.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=BASE_DIR / "akropolis_bad.png")
    parser.add_argument("--output-dir", type=Path, default=BASE_DIR / "results")
    parser.add_argument("--d", type=float, default=0.01,
                        help="Fraction at each histogram end; 0.01 = 1%%")
    parser.add_argument("--stage", choices=("histogram", "stretch"), default="stretch")
    parser.add_argument("--no-show", action="store_true", help="Save plots without windows")
    args = parser.parse_args()
    if not 0 <= args.d < 0.5:
        parser.error("--d must satisfy 0 <= d < 0.5")
    if args.no_show:
        import matplotlib
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    args.output_dir.mkdir(parents=True, exist_ok=True)
    image = open_image(args.input)
    hist = calc_histogram(image)
    plot_histogram(hist, "Histogram (original)", args.output_dir / "histogram_original.png")
    if args.stage == "stretch":
        low = calc_lower_bound(hist, args.d)
        high = calc_upper_bound(hist, args.d)
        print(f"Lower bound = {low}; upper bound = {high}; d = {args.d:g}")
        stretched = stretch_histogram(image, low, high)
        plot_histogram(calc_histogram(stretched), "Histogram (stretched)",
                       args.output_dir / "histogram_stretched.png")
        plot_images(image, stretched, args.output_dir / "comparison.png")
        write_image(stretched, args.output_dir / "akropolis_good.png")
    if not args.no_show:
        plt.show()
    plt.close("all")


if __name__ == "__main__":
    main()
