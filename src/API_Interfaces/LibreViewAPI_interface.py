from src.API_Interfaces.iAPI_interface import iAPI_interface
from src.models.LibreView.OauthResponse import LibreViewOauthResponse, User

import json
import http.client
import logging as log

class LibreViewAPI_interface(iAPI_interface):
    
    def __init__(self):
        self._get_API_key_from_envLocal("LIBREVIEW_API_KEY")
        self.conn = http.client.HTTPSConnection("api-eu.libreview.io",
                                                timeout=60)
        if self._API_KEY is None:
            log.warning(f"Unable to get the api key...you need to request oauth")
        
    def _getRequestUrl(self, endpoint:str):
        # construct request URL
        return f"{endpoint}"
    
    def requestToken(self, email:str, pswd:str):
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
            'version': '4.2.1',
            'connect-type': 'application/json',
            'Accept': "application/json"
        }
        code, jsonPlain = self._apiRequest("/llu/auth/login", "POST", 
                                           body=body, headers=headers)
        
        if code != 200:
            log.error(f"Failed to get token from LibreViewUp API ({code})")
            return code
        
        data = json.loads(jsonPlain)["data"] # convert response to dict (could be modeled if necessary)
        
        data_deserialized:LibreViewOauthResponse = \
            LibreViewOauthResponse.from_dict(data)
        
        self._API_KEY = data_deserialized.AuthTiket.Token
        
        self._setApiKey("LIBREVIEW_API_KEY", self._API_KEY)
        
        return 0
    
    def getUser(self):
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
            'Content-Type': 'application/json',
            'product': 'llu.android',
            'version': '4.2.1',
            'connect-type': 'application/json',
            'Accept': "application/json",
            'Authorization': f"Bearer {self._API_KEY}"
        }
    
        code, jsonPlain = self._apiRequest("/user", "GET", 
                                            headers=headers)

        if code != 200:
            log.error(f"Failed to get token from LibreViewUp API ({code}, {jsonPlain})")
            return code
        
        data = json.loads(jsonPlain)["data"] # convert response to dict (could be modeled if necessary)
        data_user = User.from_dict(data["user"])
        
        return 0