from src.API_Interfaces.iAPI_interface import iAPI_interface
import json
import http.client

class SpoonacularAPI_interface(iAPI_interface):
    
    def __init__(self):
        self._get_API_key_from_envLocal("SPOONACULAR_API_KEY")
        self.conn = http.client.HTTPSConnection("api.spoonacular.com")
    
    def _getRequestUrl(self, endpoint:str):
        # construct request URL
        return f"{endpoint}?apiKey={self._API_KEY}"
    
    def getRecipiesFromIngredientsList(self, ingredients: list[str], nRecipes: int = 1):
        """This method gets a list of n recipes from a list of ingredients

        Args:
            ingredients (list[str]): List of ingredients
            nRecipes (int): Number of desired recipes

        Returns:
            tuple: Request code, returned data
        """
        params:dict = {
            "ingredients": ",".join(ingredients),
            "number":nRecipes
        }
        
        code, jsonPlain = self._apiRequest("/recipes/findByIngredients", "GET", params) 
        ret = json.loads(jsonPlain) # convert response to dict (could be modeled if necessary)

        return code, ret
        