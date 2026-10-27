"""Provided helper for an image-specific per-channel lookup table."""

from dataclasses import dataclass
from enum import Enum

import numpy as np


class Channel(Enum):
    R = 0
    G = 1
    B = 2


@dataclass(frozen=True)
class CLUTEntry:
    codeword: str
    range_start: int
    range_end: int  # exclusive
    mapped_value: int
    channel: Channel


class CLUT:
    """Intervals are half-open [start, end); overlapping entries are rejected."""

    def __init__(self) -> None:
        self.entries: list[CLUTEntry] = []

    def add_entry(self, codeword: str, range_start: int, range_end: int,
                  mapped_value: int, channel: Channel) -> None:
        bits = 2 if channel is Channel.B else 3
        if len(codeword) != bits or any(c not in "01" for c in codeword):
            raise ValueError(f"{channel.name} codewords must have {bits} bits")
        if not 0 <= range_start < range_end <= 256:
            raise ValueError("Expected 0 <= start < end <= 256, got 0 <= " + str(range_start) + " < " + str(range_end) + " <= 256")
        if not 0 <= mapped_value <= 255:
            raise ValueError("Mapped value must lie in 0..255, got " + str(mapped_value))
        for entry in self.entries:
            if entry.channel is channel:
                if entry.codeword == codeword:
                    raise ValueError("Duplicate codeword in channel")
                if max(range_start, entry.range_start) < min(range_end, entry.range_end):
                    raise ValueError("Overlapping intervals in channel")
        self.entries.append(CLUTEntry(codeword, int(range_start), int(range_end),
                                      int(mapped_value), channel))

    def print_clut(self) -> None:
        for entry in self.entries:
            print(f"Channel({entry.channel.name}): "
                  f"[{entry.range_start},{entry.range_end}) --> "
                  f"{entry.mapped_value} code={entry.codeword}")

    def map_value(self, value: int, channel: Channel) -> int:
        for entry in self.entries:
            if (entry.channel is channel
                    and entry.range_start <= value < entry.range_end):
                return entry.mapped_value
        raise ValueError(f"CLUT does not cover {channel.name}={value}")

    def channel_map(self, channel: Channel) -> tuple[np.ndarray, np.ndarray]:
        """Build a small fast mapping and a coverage mask for supplied application."""
        mapping = np.zeros(256, dtype=np.uint8)
        covered = np.zeros(256, dtype=bool)
        for entry in self.entries:
            if entry.channel is channel:
                mapping[entry.range_start:entry.range_end] = entry.mapped_value
                covered[entry.range_start:entry.range_end] = True
        return mapping, covered
