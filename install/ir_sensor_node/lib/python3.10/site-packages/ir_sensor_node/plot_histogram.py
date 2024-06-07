#!/usr/bin/env python3

import matplotlib.pyplot as plt
import csv
import os
import numpy as np
from scipy.stats import norm

def main(args=None):
    home_dir = os.path.expanduser('~')
    data_dir = os.path.join(home_dir, 'ros2_ws', 'plots')
    file_path = os.path.join(data_dir, 'ir_data.csv')
    
    data = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            data.append(float(row[0]))

    # Plot the histogram of IR intensity with frequency
    plt.subplot(2, 1, 1)
    plt.hist(data, bins=50, alpha=0.75, edgecolor='black')
    plt.title('IR Intensity Histogram')
    plt.xlabel('IR Intensity')
    plt.ylabel('Frequency')

    # Fit a normal distribution to the data
    mu, sigma = norm.fit(data)
    x = np.linspace(min(data), max(data), 100)
    p = norm.pdf(x, mu, sigma)
    plt.plot(x, p, 'k', linewidth=2, label='Fit: $\mu=%.2f,\ \sigma=%.2f$' % (mu, sigma))
    plt.legend()

    # Plot the beam-based sensor model
    plt.subplot(2, 1, 2)
    beam_x = np.linspace(min(data), max(data), 100)
    beam_p = beam_sensor_model(beam_x, mu, sigma)
    plt.plot(beam_x, beam_p, 'r', linewidth=2, label='Beam-based Sensor Model')
    plt.xlabel('IR Intensity')
    plt.ylabel('Probability Density')
    plt.legend()

    plt.tight_layout()
    plt.show()

def beam_sensor_model(x, mu, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

if __name__ == '__main__':
    main()
