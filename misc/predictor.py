# from catboost import CatBoostClassifier
# import joblib
# from sklearn.preprocessing import LabelEncoder
# import numpy as np 
import pandas as pd
# import os


# loaded_encoder = joblib.load(os.path.join(os.getcwd(), "models", "w20_10_6_35.pkl"))

# model = CatBoostClassifier()
# model.load_model(os.path.join(os.getcwd(), "models", "w20_10_6_12.cbm"))


def get_prediction(inference_dataframe: pd.DataFrame) -> list:
    return [i for i in range(inference_dataframe.shape[0])]
    # y_pred = model.predict(inference_dataframe.drop('id',axis =1))
    # y_pred_decoded = loaded_encoder.inverse_transform(y=y_pred)
    # answer = pd.DataFrame({'id': inference_dataframe['id'], 
    #                        'target': y_pred_decoded})
    # return answer["target"].tolist()
