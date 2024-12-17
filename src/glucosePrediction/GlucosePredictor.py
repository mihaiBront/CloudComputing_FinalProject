from sklearn.ensemble import RandomForestRegressor
from dataclasses import dataclass, field
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
        
        sent_df = []
        sent_names = []
        for col in cols:
            sent_df.extend(df[col].values)
            sent_names.extend([f"{col}{a}" for a in appends])
                
        return [sent_names, sent_df]
        
    def predict1H(self, time_array: list | np.ndarray, glucose_array: list | np.ndarray, insulin_doses: float, carbs_gr: float):
        df = self._makeDataframe(time_array, glucose_array, insulin_doses, carbs_gr)
        return self.Model.predict(df)
        