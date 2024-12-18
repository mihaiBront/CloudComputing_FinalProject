from unittest import TestCase
from src.API_Interfaces.LibreViewAPI_interface import LibreViewAPI_interface
from src.models.LibreView.OauthResponse import OauthResponse
from src.models.LibreView.Glucose.GlucoseReadings import GlucoseReadings
from src.commons.DateTimeHelper import DateTimeHelper
from src.glucosePrediction.GlucosePredictor import GlucosePredictor

from sklearn.ensemble import RandomForestRegressor
import os
import logging as log
from dotenv import load_dotenv
import pandas as pd
import numpy as np

import logging as log
import json

class DeserializationTests(TestCase):
        
    def test_hourFromDayseconds(self):
        daySeconds = 1200
        hour = DateTimeHelper.hourFromDaysecondsInt(daySeconds)
        self.assertEqual(hour, "00:20:00")
    
    def test_deserializeJsonOauth(self):
        jsonFilePath = ".test_resources/oauth_librelink_response.json"
        if not os.path.isfile(jsonFilePath):
            log.warning(f"Test not applicable; {jsonFilePath} does not exist")
            return
        
        # arrange: read json from files
        with open(jsonFilePath, "r") as f:
            oauth_json = f.read()
        
        # act: deserialize json
        oauth_response: OauthResponse = OauthResponse.deserialize(oauth_json)
        
        # assert: check the object is filled
        self.assertIsInstance(oauth_response, OauthResponse)
        self.assertIsNotNone(oauth_response.AuthTiket)
        self.assertIsNotNone(oauth_response.User)
        log.info(f"SUCCESS object serialized correctly")
    
    def test_setKey(self):
        libreApi = LibreViewAPI_interface()
        key = "TEST_KEY"
        val = "09aa2d232d1a48c09fa6f68635eae33c"
        
        libreApi._setApiKey(key, val)
        
        try: 
            load_dotenv(".env.local")
            val_stored = os.getenv(key)
            print(f"{val_stored}|{val}")
            self.assertEqual(val, val_stored)
        except Exception as e:
            log.error(e)
            self.assertFalse(True, "Test failed")
    
    def test_deserialize_GlucoseData(self):
        jsonFilePath = ".test_resources/glucoseHistory_backup.json"
        if not os.path.isfile(jsonFilePath):
            log.warning(f"Test not applicable; {jsonFilePath} does not exist")
            return

        # arrange: read json from files
        with open(jsonFilePath, "r") as f:
            glucose_json = f.read()

        # act: deserialize json
        glucose_response = json.loads(glucose_json)["data"]
        glucose_response = GlucoseReadings.from_dict(glucose_response)

        # assert: check the object is filled
        self.assertIsInstance(glucose_response, GlucoseReadings)
        log.info(f"SUCCESS object serialized correctly")
        
    def test_getTodaysDate(self):
        log.info(DateTimeHelper.getTimestampNow())
        
    def test_glucosePredictorLoadObject(self):
        predictor = GlucosePredictor(PathToModel="reggressionGlucoseSimple.joblib")
        predictor.loadModel()
        self.assertIsInstance(predictor.Model, RandomForestRegressor)
        
    def test_glucosePredictorPredict(self):
        predictor = GlucosePredictor(PathToModel="reggressionGlucoseSimple.joblib")
        predictor.loadModel()
        
        data = pd.read_csv(".test_resources/dumpGraph/test_synthetic.csv")
        
        prediction = predictor.predict1H(data["time"].values, data["glucose"].values, 2.5, 60)
        log.info(f"Prediction: {prediction} (type={type(prediction)}, length={prediction.shape})")
        self.assertIsInstance(prediction, np.ndarray)
        
    def test_glucosePredictionSim(self):
        predictor = GlucosePredictor(PathToModel="reggressionGlucoseSimple.joblib")
        predictor.loadModel()
        
        data = pd.read_csv(".test_resources/dumpGraph/test_synthetic.csv")
        
        prediction = predictor.simulatePrediction(data["time"].values, data["glucose"].values, 2.5, 60)
        self.assertIsInstance(prediction, dict)
        self.assertIsInstance(prediction["time"], list)
        self.assertIsInstance(prediction["glucose"], list)
        
    