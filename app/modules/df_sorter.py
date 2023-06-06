# The purpose of this module is to sort the columns in the dataframe to match the order of which the SVM model was fitted
# The order is as follows
# 1. crossing_interval
# 2. mean_crossings
# 3. std_dev
# 4. std_ratio_next
# 5. std_ratio_prev


def df_sorter(df):
    return df[['crossing_interval', 'mean_crossings', 'std_dev', 'std_ratio_next', 'std_ratio_prev', 'avg_lat', 'avg_long']]
