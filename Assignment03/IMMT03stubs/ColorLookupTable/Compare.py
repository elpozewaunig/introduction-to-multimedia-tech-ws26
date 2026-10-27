import numpy as np
from PIL import Image
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
from Histogram import histogram



def read_image(path: str | Path) -> np.ndarray:
    """Return a writable uint8 RGB array, shape (height, width, 3).

    TODO: open with Pillow, convert explicitly to 'RGB', create an independent
    NumPy array, and close the Pillow image (e.g. with a context manager).
    """
    with Image.open(path).convert("RGB") as image:
        return np.array(image)


base = read_image(BASE_DIR / "mandrill_512x512.png")
recon =read_image(BASE_DIR / "mandrill_512x512_reconstructed_opt.png")
s =0
bhist =[]
rhist = []
for y, row in enumerate(base):
    for x, pixel in enumerate(row):
        if recon[y][x] != pixel:
            s +=1
            bhist.append(pixel)
            rhist.append(recon[y][x])

    print(s)
    histogram.plot_histogram(bhist, "Histogram (base)","histogram_stretched.png")
    histogram.plot_histogram(rhist, "Histogram (recon)","histogram_stretched.png")


