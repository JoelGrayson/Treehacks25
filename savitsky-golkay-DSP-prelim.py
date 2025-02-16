import numpy as np
from scipy.signal import savgol_filter
import time
# import random

sampling_rate = 250  
window_size = 11  
poly_order = 3  

buffer = []

def process_eeg_stream(new_sample):
    """
    Processes real-time EEG data using Savitzky-Golay smoothing.
    """
    global buffer
    buffer.append(new_sample)

    if len(buffer) > window_size:
        buffer.pop(0)

    if len(buffer) >= window_size:
        smoothed_signal = savgol_filter(buffer, window_size, poly_order)
        return smoothed_signal[-1] 
    else:
        return new_sample

# for _ in range(100):
#     #raw_eeg = np.sin(2 * np.pi * 1.2 * time.time()) + 0.2 * np.sin(2 * np.pi * 10 * time.time()) + random.uniform(-0.1, 0.1)
#     smoothed_eeg = process_eeg_stream(raw_eeg)
    
#     print(f"Raw EEG: {raw_eeg:.3f}, Smoothed EEG: {smoothed_eeg:.3f}")
#     time.sleep(1/sampling_rate)
