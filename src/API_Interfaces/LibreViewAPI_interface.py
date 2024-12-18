from src.API_Interfaces.iAPI_interface import iAPI_interface
from src.models.LibreView.OauthResponse import OauthResponse, User
from src.models.LibreView.Glucose.GlucoseReadings import GlucoseReadings
from src.commons.DateTimeHelper import DateTimeHelper

import json
import http.client
from dataclasses import dataclass, field
import numpy as np
from datetime import timedelta

import os
import logging as log

DEBUG = False


@dataclass
class LibreViewAPI_interface(iAPI_interface):
    _ACCOUNT_ID:str = field(default_factory=str)
    
    _PatientId:str = field(default_factory=str)
    PatientName:str = field(default_factory=str)
    
    def __init__(self):
        self._get_API_key_from_envLocal("LIBREVIEW_API_KEY")
        self._get_Account_Id_from_envLocal()
        self.conn = http.client.HTTPSConnection("api-eu.libreview.io",
                                                timeout=60)
        if self._API_KEY is None:
            log.warning(f"Unable to get the api key...you need to request oauth")
        
        self._updatePatientParams()
    
    def _get_Account_Id_from_envLocal(self):
        self._ACCOUNT_ID = self._get_envLocal("LIBREVIEW_ACCOUNT_ID")
        return
    
    def _getRequestUrl(self, endpoint:str):
        # construct request URL
        return f"{endpoint}"
    
    def _buildHeaders(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
            'Content-Type': 'application/json',
            'product': 'llu.android',
            'version': '4.11.0',
            'connect-type': 'application/json',
            'Accept': "application/json",
        }
        
        if self._API_KEY is not None:
            headers["Authorization"] = f"Bearer {self._API_KEY}"
            
        if self._ACCOUNT_ID is not None:
            headers["Account-Id"] = self._ACCOUNT_ID
            
        return headers
    
    def _updatePatientParams(self):
        if self._API_KEY is None:
            log.error("API_KEY is not set")
            return -1
        
        code, patient = self.getUser()
            
        if code != 200:
            log.error(f"Failed to get user from LibreViewUp API ({code})")
            return -2
        
        self._PatientId = patient.UserID
        self.PatientName = f"{patient.FirstName} {patient.LastName}"
        
        return 0
    
    def _buildBaseHeaders(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
            'Content-Type': 'application/json',
            'product': 'llu.android',
            'version': '4.10',
            'connect-type': 'application/json',
            'Accept': "application/json"
        }
        
        if self._API_KEY is not None:
            headers["Authorization"] = f"Bearer {self._API_KEY}"
            
        return headers
    
    def oAuth(self, email:str, pswd:str):
        """Requests an authorization from user and password

        Args:
            email (str): Email addres
            pswd (str): Password
        
        Returns:
            int: Request code or 0 if all was successful (web code 200)
        """
                        
        body = {
            "email": email,
            "password": pswd
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
            'Content-Type': 'application/json',
            'product': 'llu.android',
            'version': '4.10',
            'connect-type': 'application/json',
            'Accept': "application/json"
        }
        code, jsonPlain = self._apiRequest("/llu/auth/login", "POST", 
                                           body=body, headers=headers)
        
        if code != 200:
            log.error(f"Failed to get token from LibreViewUp API ({code})")
            return code
        
        data = json.loads(jsonPlain)["data"] # convert response to dict (could be modeled if necessary)
        
        data_deserialized:OauthResponse = \
            OauthResponse.from_dict(data)
        
        self._API_KEY = data_deserialized.AuthTiket.Token
        
        self._setApiKey("LIBREVIEW_API_KEY", self._API_KEY)
        
        self._updatePatientParams()
        
        return 0
    
    def getUser(self):
        """Gets user information from the API

        Returns:
            int: Return code
            User | str : Object of the 'User' class if the function was successful, otherwise an error message
        """
        
        headers = self._buildBaseHeaders()
    
        code, jsonPlain = self._apiRequest("/user", "GET", 
                                            headers=headers)
        user = jsonPlain      
        
        if code != 200:
            log.error(f"Failed to get token from LibreViewUp API (code {code}, message {jsonPlain})")
        else:        
            try:
                # convert response to dict (could be modeled if necessary)
                user = User.from_dict(json.loads(jsonPlain)["data"]["user"])                 
            except Exception as e:
                log.error(f"Failed to get user from LibreViewUp API (exception {e})")
                
        return code, user
    
    def getLastWeekMeasurement(self, num_periods: int = 1, period = 7):
           
        headers = self._buildBaseHeaders()
        
        params = {
            "numPeriods": num_periods,
            "period": period
        }
        
        code, data = self._apiRequest(f"/glucoseHistory", "GET",
                                    headers=headers, params=params)
        
        if code != 200:
            log.error(f"Failed to get graph from LibreViewUp API ({code})")
        else:
            if DEBUG:
                if not os.path.exists(".test_resources"): os.mkdirs(".test_resources")
                with open(".test_resources/glucoseHistory.json", "w") as f:
                    f.write(data)
                
        return code, json.loads(data)["data"]
    
    def simulateGettingRealTimeMeasurements(self):
        """Simulates the process of getting real-time measurements from the API. Pending real real time
        measurement API development, this function gets historic average from last week's data, and trans-
        forms it so it appears it is from the moment of the request.

        Returns:
            int: Return code
            dict: Dictionary containing the simulated real-time measurements
        """

        code, data = self.getLastWeekMeasurement()

        if code != 200:
            log.error(f"Failed to get graph from LibreViewUp API ({code})")
            return code, data

        data = GlucoseReadings.from_dict(data)
        
        # get curve data (Percentile50 = Average Curve; tiem = xAxis labels)
        last_period = data.Periods[-1].Data.Blocks
        curve = last_period.Percentile50
        time = last_period.Time
        
        # rearrange the vectors so the data follows this format:
        #   - Data represents the last 24h
        #   - Last measurement is the closest before the current timestamp
        #   - First measurement is the closest after the current timestamp
        #   - Modify the timestamp to account for today's date

        now = DateTimeHelper.getTimestampNow()
        # get the index of the last measurement after the current timestamp
        index = -1
        for i in range(len(time)):
            ts = DateTimeHelper.dateTimeFromStr(time[i])
            if ts.time() > now.time():
                index = i
                break
        
        if index == -1:
            log.error(f"Failed to get the index of the last measurement after the current timestamp")
            return -1, {"message":"Failed to get the index of the last measurement after the current timestamp"}
        
        # edit curve and time vectors
        curve = np.concat((curve[index:-1],curve[:index]), axis=0)
        time = time[index:-1] + time[:index]
        
        # adjusting date issues (after making that swap, the dates from the measurements
        # previous to midnight have to bee set to (TODAY-1DAY).date and the ones from after
        # that have to be set to TODAY.date())
        time = [DateTimeHelper.changeDatePartString(t, now - timedelta(days=1)) 
                    if DateTimeHelper.dateTimeFromStr(t).time() > now.time()
                    else DateTimeHelper.changeDatePartString(t, now) 
                for t in time]      
        
        # build dictionary with the graph data
        graphdata = {
            "glucose": curve,
            "time": time
        }
        
        return code, graphdata