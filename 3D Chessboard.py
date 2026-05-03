import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# 1. Setup coordinates (Higher resolution for smoother surfaces)
x = np.linspace(-4, 4, 100)
y = np.linspace(-4, 4, 100)
X, Y = np.meshgrid(x, y)

# 2. Define your function
def chess_surface(x, y):
    return (1 - x / 2 + x ** 5 + y ** 6) * np.exp(-(x ** 2 + y ** 2))

Z = chess_surface(X, Y)

# 3. Create a 3D plot
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(10, 7))

# Plot the surface
# 'antialiased=False' can make it render faster
surf = ax.plot_surface(X, Y, Z, cmap=cm.magma, linewidth=0, antialiased=True)

# 4. Add a "Chessboard" floor (Optional but cool)
# We place it at the minimum Z value so it sits underneath
ax.contourf(X, Y, Z, zdir='z', offset=np.min(Z)-0.5, cmap='binary_r', alpha=0.3)

# Add titles and labels
ax.set_title("3D Mathematical Chess Landscape")
ax.set_zlabel("Function Height")
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()