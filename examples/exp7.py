import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Data from the image
W_cm = np.array([8.0, 9.0, 10.0, 11.0, 15.0, 13.0, 6.0, 5.0, 4.0, 3.0])
X_cm = np.array([16.0, 17.7, 19.1, 19.4, 23.4, 21.5, 13.4, 11.9, 10.4, 7.7])

# Define the quadratic function
def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

# Fit the curve
params, _ = curve_fit(quadratic, W_cm, X_cm)

# Generate points for plotting the fit
W_fit = np.linspace(min(W_cm), max(W_cm), 500)
X_fit = quadratic(W_fit, *params)

# Plot the data and the fit
plt.figure(figsize=(10, 6))
plt.scatter(W_cm, X_cm, label='Data points', color='blue')
plt.plot(W_fit, X_fit, label=f'Fit: $h = {params[0]:.2f}W^2 + {params[1]:.2f}W + {params[2]:.2f}$', color='red')
plt.xlabel('W (cm)')
plt.ylabel('X (cm)')
plt.title('Quadratic Fit to h-X Data')
plt.legend()
plt.grid(True)
plt.show()