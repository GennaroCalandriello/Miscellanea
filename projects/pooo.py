import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Define the dispersion relation (refractive index as a function of wavelength)
def refractive_index(wavelength):
    # This is a simple linear approximation
    return 1.5 - (wavelength - 500) * 0.0001


# Define the prism (as a sequence of line segments)
prism = np.array([[0, 0], [1, 1], [2, 0], [0, 0]])

# Prepare the figure
fig, ax = plt.subplots()
ax.set_xlim(-1, 30)
ax.set_ylim(-1, 20)

# Prepare the lines (one for each wavelength)
wavelengths = np.linspace(380, 750, 7)
colors = plt.cm.rainbow(np.linspace(0, 1, len(wavelengths)))
lines = [plt.Line2D([], [], color=color) for color in colors]
for line in lines:
    ax.add_line(line)


# Animation update function
def update(frame):
    for wavelength, line in zip(wavelengths, lines):
        # Calculate the refracted direction
        n = refractive_index(wavelength)
        angle = np.arcsin(1 / n)
        direction = np.array([np.cos(angle), np.sin(angle)])

        # Calculate the path of the light ray
        path = [prism[0]]
        for segment in prism[1:]:
            displacement = segment - path[-1]
            if np.dot(displacement, direction) > 0:
                path.append(path[-1] + displacement)
            else:
                path.append(path[-1] + direction * frame)

        # Update the line data
        line.set_data(*zip(*path))


# Create the animation
animation = FuncAnimation(fig, update, frames=np.linspace(0, 2, 100), interval=100)

# Display the animation
plt.show()
