"""Provided histogram display. No changes required."""

from pathlib import Path

import numpy as np


def plot_histogram(hist: np.ndarray, title: str, destination: Path):
    """Plot the supplied 256 bin counts; do not compute a histogram here."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 3.5), layout="constrained")
    ax.bar(np.arange(256), hist, width=1.0, color="#245b85")
    ax.set(xlabel="Gray value", ylabel="Pixel count", title=title,
           xlim=(-0.5, 255.5))
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination, dpi=150)
    return fig


def plot_images(original: np.ndarray, stretched: np.ndarray, destination: Path):
    """Use a fixed intensity scale so image contrast remains comparable."""
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(8, 5), layout="constrained")
    for ax, image, title in zip(axes, (original, stretched),
                                ("Original", "Stretched")):
        ax.imshow(image, cmap="gray", vmin=0, vmax=255)
        ax.set_title(title)
        ax.axis("off")
    fig.savefig(destination, dpi=150)
    return fig
