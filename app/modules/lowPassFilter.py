from scipy.signal import butter, filtfilt

def low_pass_filter(data, cutoff_freq, sampling_rate, filter_order):

    x = data['accx'].values
    y = data['accy'].values
    z = data['accz'].values

    nyquist_freq = 0.5 * sampling_rate
    b, a = butter(filter_order, cutoff_freq/nyquist_freq, btype='lowpass')
    filtered_data_x = filtfilt(b, a, x, axis=0)
    filtered_data_y = filtfilt(b, a, y, axis=0)
    filtered_data_z = filtfilt(b, a, z, axis=0)

    data['accx'] = filtered_data_x
    data['accy'] = filtered_data_y
    data['accz'] = filtered_data_z

    return data