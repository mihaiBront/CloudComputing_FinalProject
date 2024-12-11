from src.API_Interfaces.iAPI_interface import iAPI_interface
from src.models.LibreView.OauthResponse import OauthResponse, User

import json
import http.client
from dataclasses import dataclass, field

import logging as log

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
            with open(".test_resources/glucoseHistory.json", "w") as f:
                f.write(data)
                
        return code, json.loads(data)["data"]