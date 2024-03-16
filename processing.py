# processing.py


import numpy as np
import scipy.signal as sig


def bandpass_filter(samples, sample_rate):
    low = 50 / (sample_rate / 2)
    high = 3000 / (sample_rate / 2)
    coefficients = sig.iirfilter(N=4, Wn=[low, high], btype='bandpass', ftype='butter', output='sos')
    filtered_samples = sig.sosfilt(coefficients, samples)

    return filtered_samples


def normalize(samples):
    samples_float = samples.astype(np.float32)
    max_value = np.max(np.abs(samples_float))

    if max_value > 0:
        normalized_samples = samples_float / max_value
    else:
        normalized_samples = samples_float

    return normalized_samples


def trim_silence(samples, tolerance=0.03):
    start = np.where(np.abs(samples) > tolerance)[0][0]
    end = np.where(np.abs(samples) > tolerance)[0][-1]

    return samples[start:end+1]


def subdivide_samples(samples, samples_per_frame):
    num_samples = len(samples)
    num_subdivisions = num_samples // samples_per_frame

    subdivided_samples = [samples[i*samples_per_frame:(i+1)*samples_per_frame] for i in range(num_subdivisions)]

    return subdivided_samples


def smooth_values(values, window_size=3):
    smoothed = []

    for i in range(len(values)):
        start = max(i - window_size // 2, 0)
        end = min(i + window_size // 2 + 1, len(values))
        smoothed.append(sum(values[start:end]) / (end - start))

    return smoothed
