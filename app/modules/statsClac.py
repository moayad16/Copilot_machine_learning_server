import numpy as np
import pandas as pd

def get_std_dev(sample):
    return np.std(sample)


def get_std_prev_curr(sample, previous_sample):
    return np.std(sample) / np.std(previous_sample)


def get_std_curr_next(sample, next_sample):
    return np.std(sample) / np.std(next_sample)


def get_mean_crossings(index, samples):
    mean = np.mean(samples)
    crossings = 0
    for i in range(index, len(samples)+index-1):
        if (samples[i] < mean and samples[i+1] > mean) or (samples[i] > mean and samples[i + 1] < mean):
            crossings += 1
    return crossings


def get_max_mean_crossing_interval(index, samples):
    mean = np.mean(samples)
    intervals = []
    for i in range(index, len(samples)+index - 1):
        if (samples[i] < mean and samples[i + 1] > mean) or (
            samples[i] > mean and samples[i + 1] < mean
        ):
            intervals.append(i)
    if len(intervals) <= 1:
        return 0
    else:
        return max(np.diff(intervals))


def extract_features(df, sample_size):
    features = []
    # print(amplitude.keys())
    amplitude = df['amplitude']

    for i in range(0, len(amplitude), sample_size):
        if i == 0:
            window = amplitude.loc[0: sample_size - 1]
            prev_window = window
        else:
            window = amplitude.loc[i: i + sample_size - 1]  # 100-199
            prev_window = amplitude[i - sample_size: i - 1]

        next_window = amplitude[i: i + sample_size - 1]

        std_dev = get_std_dev(window)
        std_ratio_prev = get_std_prev_curr(window, prev_window)
        std_ratio_next = get_std_curr_next(window, next_window)

        mean_crossings = get_mean_crossings(i, window)
        crossing_interval = get_max_mean_crossing_interval(i, window)
        avg_lat = np.mean(df['lat'][i: i + sample_size - 1])
        avg_long = np.mean(df['long'][i: i + sample_size - 1])

        sample_number = i
        features.append(
            [std_dev, std_ratio_next, std_ratio_prev, mean_crossings,
                crossing_interval, avg_lat, avg_long]
        )

    features_df = pd.DataFrame(
        features,
        columns=[
            "std_dev",
            "std_ratio_next",
            "std_ratio_prev",
            "mean_crossings",
            "crossing_interval",
            "avg_lat",
            "avg_long",
        ],
    )

    ## Normalizing the features

    mean_dict = {
        "crossing_interval": 7.724771,
        "mean_crossings": 41.165138,
        "std_dev":   0.951816,
        "std_ratio_next": 1.000904,
        "std_ratio_prev":   1.119778
    }

    std_dict = {
        "crossing_interval": 3.024848,
        "mean_crossings":  18.945721,
        "std_dev":   0.594779,
        "std_ratio_next":   0.014137,
        "std_ratio_prev": 0.625300
    }

    # subtract mean and divide by std for each feature

    for feature in features_df.columns[0:5]:
        print(feature)
        features_df[feature] = (features_df[feature] - mean_dict[feature]) / std_dict[feature]


    return features_df
