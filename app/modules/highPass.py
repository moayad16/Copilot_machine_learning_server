from scipy.signal import butter, filtfilt

def high_pass_filter(data, cutoff_freq, sampling_rate, filter_order):
    nyquist_freq = 0.5 * sampling_rate
    b, a = butter(filter_order, cutoff_freq/nyquist_freq, btype='highpass')
    filtered_data = filtfilt(b, a, data, axis=0)
    return filtered_data
