from src.API_Interfaces.iAPI_interface import iAPI_interface
from src.models.LibreViewOauthResponse import LibreViewOauthResponse
import json
import http.client
import logging as log

class LibreLinkUpAPI_interface(iAPI_interface):
    
    def __init__(self):
        self._get_API_key_from_envLocal("LIBRELINKUP_API_KEY")
        
        if self._API_KEY is None:
            log.error(f"Unable to get the api key")
            exit(1)
        
        self.conn = http.client.HTTPSConnection("api-eu.libreview.io/llu",
                                                timeout=60)
    
    def _getRequestUrl(self, endpoint:str):
        # construct request URL
        return f"{endpoint}?apiKey={self._API_KEY}"
    
    def requestToken(self, email:str, pswd:str):
        
        body = {
            "email": email,
            "password": pswd
        }
        
        headers = {
            'Content-Type': 'application/json',
            'product': 'llu.android',
            'version': '4.2.1',
            'connect-type': 'application/json'
        }
                
        self.conn.request("POST", "/llu/auth/login", body, headers)
        
        res = self.conn.getresponse()
        data = res.read()
        
        data_deserialized = LibreViewOauthResponse.deserialize(data.decode("utf-8"))
        
        return data_deserialized