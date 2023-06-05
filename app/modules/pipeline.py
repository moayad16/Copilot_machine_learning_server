from app.modules.AmplitudeCalc import AmplitudeCalc
from app.modules.lowPassFilter import low_pass_filter
from app.modules.highPass import high_pass_filter
from app.modules.statsClac import extract_features
from app.modules.df_sorter import df_sorter
import joblib

svm_model = joblib.load('app/modules/svmModel/svm_model.joblib')
# cutoff_freq = 5  # Hz
# sampling_rate = 50  # Hz
# filter_order = 4

def pipeline(df):
    return (svm_model.predict(

        df.pipe(low_pass_filter, cutoff_freq=5, sampling_rate=50, filter_order=4)
        .pipe(AmplitudeCalc)
        .pipe(extract_features, sample_size=50*2)
        .pipe(df_sorter)

        ))
