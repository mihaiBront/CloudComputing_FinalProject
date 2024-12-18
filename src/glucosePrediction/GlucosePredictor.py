from sklearn.ensemble import RandomForestRegressor
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import joblib
import numpy as np
import pandas as pd

@dataclass
class GlucosePredictor(object):
    PathToModel: str = field(default_factory=str)
    Model: RandomForestRegressor = field(default_factory=RandomForestRegressor)
    
    def loadModel(self):
        """Loads the model from the specified path"""
        self.Model = joblib.load(self.PathToModel)
        
    def _convertGlucose_mgDl_to_mmolL(self, glucose_mgDl: float):
        # Convert glucose from mg/dL to mmol/L
        return glucose_mgDl / 18.0182
    
    def _convertGlucose_mmolL_to_mgDl(self, glucose_mgDl: float):
        # Convert glucose from mg/dL to mmol/L
        return glucose_mgDl * 18.0182
        
    def _makeDataframe(self, time_array: list | np.ndarray, glucose_array: list | np.ndarray, insulin_doses: float, carbs_gr: float):
        if len(time_array) != len(glucose_array):
            raise Exception("time_array and glucose_array must have the same length")
        
        # make insulin time array
        insulin_array = np.zeros_like(glucose_array)
        insulin_array[-1] = insulin_doses
        
        carbs_array = np.zeros_like(glucose_array)
        carbs_array[-1] = carbs_gr
        
        _glucose_array = self._convertGlucose_mgDl_to_mmolL(glucose_array)
           
        # make a dictionary for creating a dataframe
        data = {
            "time": time_array,
            "bg": _glucose_array,
        }
        
        # make base dataframe
        df = pd.DataFrame(data)
        df["time"] = pd.to_datetime(df["time"])

        df.sort_values(by="time", inplace=True)
        
        df["insulin"] = insulin_array
        df["carbs"] = carbs_array
        
        # interpollate to 5min intervals
        df = df.set_index("time").resample("5T").interpolate(method="linear").reset_index()
        df.sort_values(by="time", inplace=True, ascending=False)
        
        # filter only the interest rows (intervals of 15min for the model, starting from the end; and for a maximum of 6h)
        df = df[::3][:24]
        
        df.set_index("time", inplace=True)
        
        hm = [((15*i)//60, str((15*i)%60).zfill(2)) for i in range(24)]
        
        df["appends"] = [f"-{h[0]}:{h[1]}" for h in hm]
        
        # make the dataframe for the predictor. For each column-append combination, make one column to the new dataframe

        # sent_df = pd.DataFrame()
        appends = df["appends"].values
        df.drop(columns=["appends"], inplace=True)
        cols = df.columns
        
        sent_data = []
        sent_names = []
        for col in cols:
            sent_data.extend(df[col].values)
            sent_names.extend([f"{col}{a}" for a in appends])
        
        sent_df = pd.DataFrame([sent_data], columns=sent_names)            
                
        return sent_df
    
    def predict1H(self, time_array: list | np.ndarray, glucose_array: list | np.ndarray, insulin_doses: float, carbs_gr: float):
        df = self._makeDataframe(time_array, glucose_array, insulin_doses, carbs_gr)
        try:
            prediction = self.Model.predict(df)
            prediction = np.array([self._convertGlucose_mmolL_to_mgDl(pred) for pred in list(prediction)[:]])
            return prediction
        except Exception as ex:
            raise Exception(f"Model prediction failed: {ex}")
        
    def simulatePrediction(self, time_array: list | np.ndarray, glucose_array: list | np.ndarray, insulin_doses: float, carbs_gr: float):
        # get predictuon
        try:
            prediction = self.predict1H(time_array, glucose_array, insulin_doses, carbs_gr)
        except Exception as ex:
            raise Exception(f"Simulation prediction failed: {ex}")
        
        if len(prediction) > 1:
            prediction = list([float(prediction[0])])
        
        # generate prediction array
        predTime = datetime.strptime(sorted(time_array)[-1], "%Y-%m-%d %H:%M:%S") + timedelta(hours=1)        
        
        colsForInterp = 12
        
        list_time = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in time_array[-colsForInterp:]]
        list_time.append(predTime)
        
        list_glucose = glucose_array[-colsForInterp:].tolist()
        list_glucose.append(prediction[0])
        
        pred_df = pd.DataFrame() # dataframe for the prediction interpolation
        pred_df["time"] = list_time
        pred_df["glucose"] = list_glucose
        pred_df = pred_df.set_index("time").resample("10    T").interpolate(method="cubic").reset_index()
        pred_df["time"] = pred_df["time"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
        
        # generate prediction points
        ret_pred = {
            "time": list(pred_df["time"])[-12:],
            "glucose": list(pred_df["glucose"][-12:])
        }
        
        return ret_pred