from dotenv import load_dotenv
import os
import http.client
import json

import logging as log

class iAPI_interface(object):
    conn: http.client.HTTPSConnection | None = None
    delimiter:str = "&"
    
    _API_KEY: str | None = None
    _APP_ID: str | None = None
    
    def _variableToRequestUrlParam(self, value):
        """ This method converts different types instances into strings
        to be fit as parameters in the request URL.

        Args:
            value (any): The value to be converted to a string.

        Returns:
            str: The string representation of the value. 
        """
        match(value):
                case list():
                    _ret = ",".join(value)
                case _:
                    _ret = value
        return _ret
    
    def _getRequestUrl(self, endpoint):
        """ This method returns a request URL for a specific endpoint. Adding the necessary
        API key and other parameters to the URL

        Args:
            endpoint (str): The endpoint for which the request URL is to be constructed.

        Returns:
            str: The request URL for the specified endpoint.
        """
        
        log.error("This method is not defined")
        return None
    
    def _apiRequest(self, endpoint:str, method:str, params:dict = {}, body: dict|None = {}, headers: dict = {}):
        """ This method sends an API request to the specified endpoint using the provided parameters.

        Args:
            endpoint (str): The endpoint to which the request is to be sent.
            method (str): The HTTP method to be used for the request.
            params (dict, optional): The parameters to be included in the request URL. Defaults to {}.
            body (dict, optional): The body of the request. Defaults to {}.
            headers (dict, optional): The headers to be included in the request. Defaults to {}.

        Returns:
            tuple: A tuple containing the response code and the response data.
        """
        
        if self.conn is None:
            log.error("Connection not initialized")
            return None
        
        requestUrl: str = self._getRequestUrl(endpoint)
        
        for key, value in params.items():
            requestUrl += \
                f"{self.delimiter}{key}={self._variableToRequestUrlParam(value)}"
        
        _body = json.dumps(body)
        
        self.conn.request(method, requestUrl, 
                            _body, headers)
        
        res = self.conn.getresponse()
        data = res.read()
        ret = data.decode("utf-8")
        
        return res.code, ret
    
    def _get_APPid_from_envLocal(self, entryName: str):
        """Gets the APP name from your local environment file, which must
        be placed in a '.env.local' file in your root directory'
        This function must be called from the constructors of the classes 
        implementing this interface.

        Args:
            entryName (str): Name of the key storing the APP name for a speciffic API.
        """        
        try:
            load_dotenv(dotenv_path='.env.local')
            self._APP_ID = os.getenv(entryName)
        except Exception as ex:
            log.error(f"Failed getting key from environment ({ex})") 
    
    def _get_API_key_from_envLocal(self, entryName: str):
        """Gets the API key from your local environment file, which must be placed in a '.env.local' file in your root directory'
        This function must be called from the constructors of the classes implementing this interface.
        
        Args:
            entryName (str): Name of the key storing the API key for a speciffic API.
        """        
        try:
            load_dotenv(dotenv_path='.env.local')
            self._API_KEY = os.getenv(entryName)
        except Exception as ex:
            log.error(f"Failed getting key from environment ({ex})")