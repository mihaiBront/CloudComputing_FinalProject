from src.apiInterfaces.iAPI_interface import iAPI_interface
import json
import logging as log
import http.client

class edamamAPI_interface(iAPI_interface):
        
    def __init__(self):
        self._get_API_key_from_envLocal("EDAMAM_APP_KEY")
        self._get_APPid_from_envLocal("EDAMAM_APP_ID")
        self.conn = http.client.HTTPSConnection("api.edamam.com")
        
    def _getRequestUrl(self, endpoint:str):
        # construct request URL
        return f"{endpoint}?app_id={self._APP_ID}{self.delimiter}app_key={self._API_KEY}"
            
    def gtetNutritionalTableFromIngredients(self, recipeName: str, ingredients: list[str], servings: str = ""):
        """_summary_

        Args:
            recipeName (str): _description_
            ingredients (list[str]): _description_
            servings (str, optional): _description_. Defaults to "".

        Returns:
            _type_: _description_
        """
        
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