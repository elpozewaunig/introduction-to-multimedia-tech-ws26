# Optional array quick reference

The exercises require basic NumPy arrays, not advanced NumPy programming.
Ordinary loops are a complete, acceptable way to solve them. This page is a
reference for library syntax; it adds no assignment tasks.

## Pixels and arithmetic

```python
import numpy as np

height, width = image.shape[:2]
gray = int(image[y, x])       # grayscale image
red = int(image[y, x, 0])    # RGB image: channels 0=R, 1=G, 2=B
image[y, x, 0] = 120        # write one RGB channel
```

Use `for y in range(height)` and `for x in range(width)` for pixel loops.
The axis order is `[y, x]`, unlike APIs whose pixel methods take `(x, y)`.
Use Python `int(...)` before arithmetic on an individual `uint8` value.
Python integers can represent negative values and intermediate results above 255.
Before writing a final channel value, clip it to 0–255 and round as specified
in the worksheet. For array-wide arithmetic, `image.astype(np.float64)` makes
an independent floating-point array instead.

## Create arrays and copies

```python
counts = np.zeros(256, dtype=np.int64)           # 256 integer counters
gray_output = np.empty((height, width), dtype=np.uint8)
rgb_output = np.empty((height, width, 3), dtype=np.uint8)
same_shape = np.empty_like(image)
independent_copy = image.copy()
```

Write every element of an `empty` array before reading it. `other = image`
creates another reference to the same array, not a copy.
NumPy arrays store fixed-width values; `uint8` stores 0–255. This is different
from Python's ordinary integers and from signed 8-bit types.

## Sorting and slices

```python
values = np.array([9, 2, 7, 2], dtype=np.uint8)
ordered = np.sort(values)       # new array: [2, 2, 7, 9]
first_two = ordered[:2]         # indices 0 and 1; end index is excluded
remaining = ordered[2:]        # indices 2 through the end
```

`len(values)` gives the length of a 1-D array; `image.size` counts all elements.
`array.reshape(-1)` flattens an array. `image[:, :, 0]` selects all red samples.
Slices may share storage with their source. Use `.copy()` if you need to modify
a slice without affecting the source. Sorting/splitting read-only samples does
not require additional copies.

The annotations such as `image: np.ndarray` and `-> int` describe expected
types. They are supplied and need not be changed. The `main()` function and
`if __name__ == "__main__":` start each script; that framework is also supplied.
