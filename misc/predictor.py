from catboost import CatBoostClassifier
import joblib
from sklearn.preprocessing import LabelEncoder
import numpy as np 
import pandas as pd


loaded_encoder = joblib.load('models\\w20_10_6_35.pkl')

model = CatBoostClassifier()
model.load_model("models\\w20_10_6_12.cbm")


def get_prediction(inference_dataframe: pd.DataFrame) -> list:
    # y_pred = model.predict(inference_dataframe.drop('id',axis =1))
    y_pred = model.predict(inference_dataframe)
    y_pred_decoded = loaded_encoder.inverse_transform(y=y_pred)
    answer = pd.DataFrame({'id': inference_dataframe['id'], 
                           'target': y_pred_decoded})
    return answer["target"].tolist()