import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path


# TODO: Make argument parsable

# Hull fixed values, change these to the spec of your project
a = 50     # Nose length [mm]
b = 426   # Cylinder length [mm]
c = 80     # Length of tail [mm]
d = 114     # Diameter of cylindrical section [mm]

# The tail section cuts off at diameter of the rotor hub
propeller_diameter = 36


# Design parameters, choose this according to your needs
n = 2                   # Nose shape parameter
theta = 10 * np.pi/180  # Tail shape parameter [rad]
resolution = 0.5        # Curve resolution [mm]


def nose(x):
    return 1/2 * d * (1 - ((x-a)/a)**2)**(1/n)


def tail(x):
    return 1/2*d - ((3*d)/(2*c**2) - np.tan(theta)/c)*x**2 + (d/(c**3) - np.tan(theta)/(c**2))*x**3


y = d
tail_cutoff = 0
while y > propeller_diameter/2:
    tail_cutoff += 1
    y = tail(tail_cutoff)

print(f"Tail cutoff: {tail_cutoff}")

# Vectorize for efficiency
nose_func = np.vectorize(nose)
nose_length = np.linspace(0, a, int(a*resolution))

tail_func = np.vectorize(tail)
# tail_length = np.linspace(0, c, int(c*resolution))
tail_length = np.linspace(0, tail_cutoff, int(tail_cutoff*resolution))

# Fusion 360 requires correct formatting and reads 0.1 as 1mm
nose_spline = np.stack([nose_length, nose_func(
    nose_length), np.zeros(nose_length.shape)], axis=1)/10

# Format save path
format = "%Y-%M-%d-%H-%M-%S"
now = datetime.now()
time_stamp = now.strftime(format).replace(" ", "")
nose_save_path = f"{Path.home()}/Downloads/myring-nose-{time_stamp}.csv"

# Save to CSV
np.savetxt(nose_save_path, nose_spline, delimiter=",")
print(f"Saved as: {nose_save_path}")

# Fusion 360 requires correct formatting and reads 0.1 as 1mm
tail_spline = np.stack([tail_length, tail_func(
    tail_length), np.zeros(tail_length.shape)], axis=1)/10

# Save to given path
tail_save_path = f"{Path.home()}/Downloads/myring-tail-{time_stamp}.csv"
np.savetxt(tail_save_path, tail_spline, delimiter=",")
print(f"Saved as: {tail_save_path}")

# Plot
plt.gca().set_aspect('equal', adjustable='box')

print(nose_spline)
plt.plot(nose_length, nose_func(nose_length))

print(tail_spline)
plt.plot(tail_length, tail_func(tail_length))

# Show
plt.show()
