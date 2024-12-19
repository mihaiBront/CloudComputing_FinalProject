from dotenv import load_dotenv, set_key
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
    
    @staticmethod
    def _setApiKey(key:str, value:str, env_path: str = ".env.local"):
        """ This method sets the API key in the environment file.

        Args:
            key (str): The key to be set in the environment file.
            value (str): The value of the key to be set.
            env_path (str, optional): The path to the environment file. Defaults to ".env.local".
        """
        
        load_dotenv(dotenv_path=env_path)
        path = ".env.local"
        set_key(path, key, value)
        return
    
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
        
        if not("?" in requestUrl):
            requestUrl += "?"
        else:
            requestUrl += self.delimiter
        
        for key, value in params.items():
            requestUrl += \
                f"{key}={self._variableToRequestUrlParam(value)}{self.delimiter}"
        
        requestUrl = requestUrl[:-1]
        
        _body = json.dumps(body)
        
        self.conn.request(method, requestUrl, 
                            _body, headers)
        
        res = self.conn.getresponse()
        data = res.read()
        ret = data.decode("utf-8")
        
        return res.code, ret
    
    def _get_envLocal(self, key):
        """Gets the value of a key from your local environment file, which must be placed in a '.env.local' file in your root directory'

        Args:
            key (str): The key to be retrieved from the environment file.

        Returns:
            str: The value of the key.
        """
        try:
            load_dotenv(dotenv_path='.env.local')
            return os.getenv(key)
        except Exception as ex:
            log.error(f"Failed getting key from environment ({ex})")
            return None
    
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