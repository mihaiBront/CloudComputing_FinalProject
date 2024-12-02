from src.apiInterfaces.iAPI_interface import iAPI_interface
import json
import logging as log
import http.client

class edamamAPI_interface(iAPI_interface):
        
    def __init__(self):
        self._get_API_key_from_envLocal("EDAMAM_APP_KEY")
        self._get_APPid_from_envLocal("EDAMAM_APP_ID")
        self.conn = http.client.HTTPSConnection("api.edamam.com")
    
    def _variableToRequestUrlParam(self, value):
        match(value):
                case list():
                    _ret = ",".join(value)
                case _:
                    _ret = value
        return _ret
    
    def _apiRequest(self, endpoint:str, method:str, params:dict = {}, body: dict|None = {}, headers: dict = {}):
        # construct request URL
        requestUrl: str = f"{endpoint}?app_id={self._APP_NAME}{self.delimiter}app_key={self._API_KEY}"
        
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
    
    def gtetNutritionalTableFromIngredients(self, recipeName: str, ingredients: list[str], servings: str = ""):
        body:dict = {
            "title": recipeName,
            "ingr": ingredients,
            "yield": servings
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        code, jsonPlain = self._apiRequest("/api/nutrition-details", "POST", body=body, headers=headers) 
        ret = json.loads(jsonPlain) # convert response to dict (could be modeled if necessary)

        return code, ret