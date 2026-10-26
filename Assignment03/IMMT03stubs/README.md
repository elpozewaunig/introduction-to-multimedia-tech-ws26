# Assignment 03 — Python stubs

Use Python 3.12 or newer. Run the commands below from this directory.

## Setup

Create and activate a virtual environment:

```text
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```sh
source .venv/bin/activate
```

Then install the dependencies:

```text
python -m pip install -r requirements.txt
```

`requirements-tested.txt` records the exact versions used to verify this
assignment. To reproduce that environment, install it instead of
`requirements.txt`.

If PowerShell does not allow activation, use `.\.venv\Scripts\python.exe`
instead of `python` in the remaining commands. No change to the execution
policy is necessary.

## Image representation

- Pillow reads/writes files; NumPy arrays represent images in the algorithms.
- Grayscale: shape `(height, width)`, `dtype=np.uint8`, values 0–255.
- RGB: shape `(height, width, 3)`, `dtype=np.uint8`, channel order R, G, B.
- Access pixels as `image[y, x]`; access a channel as `image[y, x, channel]`.
- An RGB332 image has shape `(height, width)` and `dtype=np.uint8`.
  Its bytes are color codes, **not grayscale intensities**.
- Use Python `int` or a wider/float array for arithmetic. Convert to `uint8`
  only after clipping and rounding. Use `image.copy()` for an independent copy.

## Your tasks

Implement only the functions marked `TODO`. Their docstrings define the
contracts. The program flow, plotting, and CLUT helper are provided.
The stubs deliberately raise `NotImplementedError` until completed.

Implement the histogram, bounds, stretching, RGB332 quantization/reconstruction,
and recursive LUT construction yourself. Do not replace these tasks with
`Image.histogram`, `ImageOps.autocontrast`, `Image.quantize`, `np.histogram`,
`np.bincount`, or `np.quantile` / `np.percentile`. Array indexing, sorting,
slicing, allocation, basic arithmetic, and clipping are allowed; loops are fine.
Straightforward pixel loops are sufficient. Vectorization and runtime optimization
are not required or assessed. No NumPy knowledge beyond basic array operations is
assumed; `ARRAY_GUIDE.md` is an optional quick reference, also for students coming
from Java. You do not need to modify the plotting code, command-line handling,
or CLUT helper classes.

### Histogram

After implementing `open_image` and `calc_histogram`, run:

```text
python Histogram/main.py --stage histogram
```

After implementing the remaining functions, run:

```text
python Histogram/main.py --d 0.01
```

`d` is a fraction **at each end**: `0.01` means 1% below and 1% above.
Set `q = floor(d * N)` where `N` is the number of pixels. Scan from each
end of the histogram and select the first occupied bin for which the cumulative
count is **strictly greater** than `q`. Require `0 <= d < 0.5`.
The equal-bound case is provided. Otherwise clip the linear
transformation to 0–255 and round with `floor(value + 0.5)`.

The provided plotting code creates all figures before calling `show()` once.
If no graphical backend is available, use:

```text
python Histogram/main.py --d 0.01 --no-show
```

Images and plots are also saved under `Histogram/results/`. An optional
`--input PATH` accepts another image and `--output-dir PATH` changes the
destination. Default paths are relative to the script, not your working directory.

### Simple RGB332 quantization

Complete `ColorLookupTable/image_io.py` (you can reuse the histogram I/O code,
changing `L` to `RGB`) and `ColorLookupTable/eight_bit_image.py`.

```text
python ColorLookupTable/eight_bit_image.py
```

Use bit layout `RRRGGGBB`, keeping the three most significant bits of R/G and
the two most significant bits of B. Reconstruct channel codes 0–7 / 0–3 over
the full range 0–255, rounding with `floor(value + 0.5)`.
The reconstructed PNG is an RGB visualization, not an indexed PNG.

### Optimized color lookup table

Complete the two TODO functions in `ColorLookupTable/optimized_lut.py`.
The CLUT helper and its application to an image are already implemented.

```text
python ColorLookupTable/optimized_lut.py
```

Sort all samples separately per channel, preserving duplicate values. For each
recursive group, split at the upper median sample `values[len(values) // 2]`:
values below the threshold go left (`0`), the others go right (`1`). The supplied
`median_threshold(values)` handles repeated median values so both groups remain
nonempty. Handling constant groups and padding their codewords is also supplied.
Implement the recursive splitting and the leaf at zero remaining bits yourself.
The outer CLUT creation and its three initial recursive calls are provided,
as in the original project structure.

Create each leaf with the half-open interval `[min, max + 1)` and the mean sample
value rounded with `floor(mean + 0.5)`. This avoids overlapping intervals.
The LUT covers the samples of its input image; use it on that same image.
Constant channels may have fewer than 8 / 8 / 4 entries.

This exercise adapts quantization intervals separately per channel. The bit budget
remains 3/3/2; it does not create 256 freely chosen RGB palette entries.
As in the supplied program structure, the result is written as an RGB PNG.
Building a packed index image or an indexed PNG for this optimized LUT is not required.

Both color programs also accept `--input PATH` and `--output PATH`.
To compare their results visually, open the input and output PNGs.

## Files

```text
Histogram/
  main.py                  # TODO: image I/O, histogram, bounds, stretching
  histogram.py             # supplied Matplotlib display
  akropolis_bad.png
ColorLookupTable/
  image_io.py              # TODO: RGB image I/O
  eight_bit_image.py        # TODO: encode and reconstruct RGB332
  optimized_lut.py          # TODO: recursive per-channel LUT construction
  clut.py                  # supplied CLUT helper
  mandrill_512x512.png
  lena_512x512.png
  tree.jpg
  leaves.jpg
```
