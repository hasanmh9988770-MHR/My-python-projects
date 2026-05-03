import matplotlib.pyplot as plt
import numpy as np

# Setup coordinates
dx, dy = 0.015, 0.05
x = np.arange(-4.0, 4.0, dx)
y = np.arange(-4.0, 4.0, dy)
X, Y = np.meshgrid(x, y)
extent = [np.min(x), np.max(x), np.min(y), np.max(y)]

# Generate the 8x8 checkerboard pattern
# np.add.outer creates a grid of sums, % 2 creates the alternating 0/1 pattern
z1 = np.add.outer(range(8), range(8)) % 2

# Plot the background chessboard
plt.imshow(z1, cmap="binary_r", interpolation="nearest", extent=extent, alpha=1)

# Define the "Chess" function (Scalar field)
def chess(x, y):
    return (1 - x / 2 + x ** 5 + y ** 6) * np.exp(-(x ** 2 + y ** 2))

z2 = chess(X, Y)

# Overlay the function with bilinear interpolation for smoothness
plt.imshow(z2, alpha=0.7, interpolation="bilinear", extent=extent, cmap="magma")

plt.title("Chess Board with Python")
plt.colorbar(label="Function Intensity") # Added a colorbar for clarity
plt.show()