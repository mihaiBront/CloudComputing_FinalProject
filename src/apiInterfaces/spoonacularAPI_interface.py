from src.apiInterfaces.iAPI_interface import iAPI_interface
import json
import requests
import logging as log
import http.client

class spoonacularAPI_interface(iAPI_interface):
    delimiter:str = "&"
    
    def __init__(self):
        self._get_API_key_from_envLocal("SPOONACULAR_API_KEY")
        self.conn = http.client.HTTPSConnection("api.spoonacular.com")
    
    def _variableToRequestUrlParam(self, value):
        match(value):
                case list():
                    _ret = ",".join(value)
                case _:
                    _ret = value
        return _ret
    
    def _apiRequest(self, endpoint:str, requestType:str, params:dict):
        # construct request URL
        requestUrl: str = f"{endpoint}?apiKey={self._API_KEY}"
        
        for key, value in params.items():
            requestUrl += \
                f"{self.delimiter}{key}={self._variableToRequestUrlParam(value)}"
        
        payload = ''
        headers = {}
        self.conn.request(requestType, requestUrl, 
                     payload, headers)
        res = self.conn.getresponse()
        data = res.read()
        ret = data.decode("utf-8")
        
        return res.code, ret
    
    def getRecipiesFromIngredientsList(self, ingredients: list[str], nRecipes: int):
        params:dict = {
            "ingredients":ingredients,
            "number":nRecipes
        }
        
        code, jsonPlain = self._apiRequest("/recipes/findByIngredients", "GET", params) 
        ret = json.loads(jsonPlain) # convert response to dict (could be modeled if necessary)

        return code, ret
        