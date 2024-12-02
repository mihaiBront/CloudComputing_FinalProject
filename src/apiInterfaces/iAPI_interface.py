from dotenv import load_dotenv
import os
import http.client

import logging as log

class iAPI_interface(object):
    conn: http.client.HTTPSConnection | None = None
    delimiter:str = "&"
    
    _API_KEY: str | None = None
    _APP_NAME: str | None = None
    
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
            self._APP_NAME = os.getenv(entryName)
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
            
    def _apiRequest(self):
        """Method for handling any API request

        Returns:
            list: Todo: TBD
        """        
        log.error("This method is not implemented!")
        return None