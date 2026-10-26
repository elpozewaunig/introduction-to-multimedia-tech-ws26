"""Assignment 03: adaptive per-channel color quantization, with 3/3/2 bits."""

import argparse
from pathlib import Path

import numpy as np

from clut import CLUT, Channel
from image_io import read_image, write_image

BASE_DIR = Path(__file__).resolve().parent


def create_lookup_table(image: np.ndarray) -> CLUT:
    """Return an image-specific CLUT for a uint8 RGB image.

    TODO: extract all samples separately per channel, flatten and sort each
    channel (preserve duplicates), storing them in r, g, and b below.
    Do not change the input image. The recursive calls are provided.
    """
    r = np.empty(0, dtype=np.uint8)
    g = np.empty(0, dtype=np.uint8)
    b = np.empty(0, dtype=np.uint8)

    # TODO: replace the empty arrays with the sorted channel samples.
    raise NotImplementedError("Implement create_lookup_table")

    clut = CLUT()
    create_lookup_entry(r, "", 3, clut, Channel.R)
    create_lookup_entry(g, "", 3, clut, Channel.G)
    create_lookup_entry(b, "", 2, clut, Channel.B)
    return clut


def median_threshold(values: np.ndarray) -> int:
    """Provided: choose a median threshold with two nonempty groups.

    Precondition: values is sorted, nonempty, and not constant.
    The special case for repeated minimum values is handled here.
    """
    threshold = values[len(values) // 2]
    if threshold == values[0]:
        threshold = values[np.searchsorted(values, values[0], side="right")]
    return int(threshold)


def create_lookup_entry(values: np.ndarray, codeword: str, bits_left: int,
                        clut: CLUT, channel: Channel) -> None:
    """Recursively add CLUT entries for sorted, nonempty 1-D channel samples.

    TODO: if no bits remain, create a leaf; otherwise obtain a split threshold
    from the provided median_threshold(values) and split the samples.
    Left: samples < threshold, codeword + '0'. Right: samples >= threshold,
    codeword + '1'. Recurse with one fewer bit.

    At bits_left == 0, create one leaf:
      - the current codeword;
      - half-open interval [int(values[0]), int(values[-1]) + 1);
      - representative floor(mean(values) + 0.5).

    Use clut.add_entry(codeword, start, end, representative, channel).
    Return None; the supplied CLUT is filled in place.
    Handling constant groups and padding their codewords is already provided.
    """
    if values[0] == values[-1]:
        value = int(values[0])
        clut.add_entry(codeword + "0" * bits_left, value, value + 1, value, channel)
        return

    # TODO: check bits_left, then either split and recurse or add a leaf.
    raise NotImplementedError("Implement create_lookup_entry")


def use_clut(image: np.ndarray, clut: CLUT) -> np.ndarray:
    """Provided: apply a CLUT to its source image, returning a new uint8 RGB array."""
    result = np.empty_like(image)
    for channel in Channel:
        samples = image[:, :, channel.value]
        mapping, covered = clut.channel_map(channel)
        if not np.all(covered[samples]):
            raise ValueError(f"CLUT incomplete for channel {channel.name}")
        result[:, :, channel.value] = mapping[samples]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=BASE_DIR / "mandrill_512x512.png")
    parser.add_argument("--output", type=Path,
                        default=BASE_DIR / "mandrill_512x512_reconstructed_opt.png")
    args = parser.parse_args()
    image = read_image(args.input)
    clut = create_lookup_table(image)
    clut.print_clut()
    result = use_clut(image, clut)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_image(result, args.output)
    print(f"Saved RGB reconstruction to {args.output}")


if __name__ == "__main__":
    main()
