import pandas as pd
import numpy as np

def AmplitudeCalc(df):
    x = df['accx'].values
    y = df['accy'].values
    z = df['accz'].values

    # calculating the amplitude of the acceleration vector
    df['amplitude'] = np.sqrt(x**2 + y**2 + z**2)
    return df