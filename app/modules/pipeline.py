from app.modules.AmplitudeCalc import AmplitudeCalc
from app.modules.lowPassFilter import low_pass_filter
from app.modules.highPass import high_pass_filter
from app.modules.statsClac import extract_features
from app.modules.df_sorter import df_sorter
import joblib
from app.database import data

svm_model = joblib.load('app/modules/svmModel/svm_grid_96.joblib')
# model = joblib.load('app/modules/svmModel/rfc_grid.joblib')
# cutoff_freq = 5  # Hz
# sampling_rate = 50  # Hz
# filter_order = 4

def pipeline(df):

    final_df = df.pipe(AmplitudeCalc).pipe(extract_features, sample_size=100).pipe(df_sorter)
    
    results = []
    for i in range(len(final_df)):
        row = final_df.iloc[i]['crossing_interval':'std_ratio_prev'].values.reshape(1, -1)

        prediction =  svm_model.predict(row)[0]

        # Save the data to the data collection database.
        # data.insert_one({
        #     "crossing_interval": final_df.iloc[i]['crossing_interval'],
        #     "mean_crossings": final_df.iloc[i]['mean_crossings'],
        #     "std_dev": final_df.iloc[i]['std_dev'],
        #     "std_ratio_next": final_df.iloc[i]['std_ratio_next'],
        #     "std_ratio_prev": final_df.iloc[i]['std_ratio_prev'],
        #     "avg_lat": final_df.iloc[i]['avg_lat'],
        #     "avg_long": final_df.iloc[i]['avg_long'],
        #     "label": prediction
        # })


        results.append({
            "res": prediction,
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