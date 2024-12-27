import time
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import math

# Path to the executable
executable = "./proj2"

# Create a list to store the execution times and the values of f(n,m,l)
times = []
f_nml = []

# Read data from file
with open("testes.txt", "r") as out:
    for i in range(0, 249):
        line = out.readline()
        line = line.split()
        n = int(line[0])
        m = int(line[1])
        l = int(line[2])
        exec_time = float(line[3])  # Evitar conflito de nome com `time`
        
        f_nml.append(l * m + n*l - l**2)
        times.append(exec_time)

# Plot all the data
plt.scatter(f_nml, times, alpha=0.5, color="blue", label="Original Data")

# Ajust a curve of degree 2
degree = 1
coef = np.polyfit(f_nml, times, degree)
poly_fn = np.poly1d(coef)

# Calculate expected times and deviations
expected_times = poly_fn(f_nml)
errors = np.abs(np.array(times) - expected_times)

# Define a threshold for outliers (e.g., 90th percentile of the errors)
threshold = np.percentile(errors, 80)

# Filter data: keep points with errors below the threshold
filtered_indices = [i for i, error in enumerate(errors) if error <= threshold]
filtered_f_nml = [f_nml[i] for i in filtered_indices]
filtered_times = [times[i] for i in filtered_indices]

# Recalculate the curve with filtered data
filtered_coef = np.polyfit(filtered_f_nml, filtered_times, degree)
filtered_poly_fn = np.poly1d(filtered_coef)

# Plot the filtered data
#plt.scatter(filtered_f_nml, filtered_times, alpha=0.5, color="blue")

# Plot the initial curve
sorted_nml_values = sorted(f_nml)
plt.plot(sorted_nml_values, poly_fn(sorted_nml_values), '--', color="red", label="Initial Curve")

"""
# Plot the filtered curve
sorted_filtered_nml_values = sorted(filtered_f_nml)
plt.plot(sorted_filtered_nml_values, filtered_poly_fn(sorted_filtered_nml_values), '--', color="red")
"""

# Labels and legend
plt.xlabel("f(n,m,l)")
plt.ylabel("Time(s)")
plt.legend()
plt.show()
