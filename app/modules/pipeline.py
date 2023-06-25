from app.modules.AmplitudeCalc import AmplitudeCalc
from app.modules.lowPassFilter import low_pass_filter
from app.modules.highPass import high_pass_filter
from app.modules.statsClac import extract_features
from app.modules.df_sorter import df_sorter
import joblib

svm_model = joblib.load('app/modules/svmModel/rfc_grid.joblib')
# cutoff_freq = 5  # Hz
# sampling_rate = 50  # Hz
# filter_order = 4

def pipeline(df):

    final_df = df.pipe(AmplitudeCalc).pipe(extract_features, sample_size=100).pipe(df_sorter)
    
    results = []
    for i in range(len(final_df)):
        row = final_df.iloc[i]['crossing_interval':'std_ratio_prev'].values.reshape(1, -1)
        results.append({
            "res": svm_model.predict(row)[0],
            "lat": final_df.iloc[i]['avg_lat'],
            "long": final_df.iloc[i]['avg_long']
        })


    # return (svm_model.predict(

    #     df.pipe(low_pass_filter, cutoff_freq=5, sampling_rate=50, filter_order=4)
    #     .pipe(AmplitudeCalc)
    #     .pipe(extract_features, sample_size=50*2)
    #     .pipe(df_sorter)

    #     ))

    return results