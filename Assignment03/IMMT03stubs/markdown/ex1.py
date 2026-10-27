import numpy as np
from PIL import Image

# 1. Create a 3x2 RGB Pillow image (Width = 3, Height = 2)
width, height = 3, 2
pil_img = Image.new("RGB", (width, height), color=(255, 128, 64))

# 2. Convert the Pillow image to a NumPy array
np_arr = np.array(pil_img)

# --- PILLOW REPRESENTATION ---
print("=== PILLOW (PIL) IMAGE ===")
print(f"Mode:             {pil_img.mode}")
print(f"Dimensions (W,H): {pil_img.size}")             # (Width, Height)
print(f"Pixel at (x=0,y=0): {pil_img.getpixel((0, 0))}") # (R, G, B) tuple

# --- NUMPY ARRAY REPRESENTATION ---
print("\n=== NUMPY ARRAY ===")
print(f"Shape (H, W, C):  {np_arr.shape}")            # (Height, Width, Channels)
print(f"Data Type:        {np_arr.dtype}")            # uint8
print(f"Value Range:      {np_arr.min()} to {np_arr.max()}")
print(f"Pixel at [row=0, col=0]: {np_arr[0, 0]}")     # [R, G, B] ndarray