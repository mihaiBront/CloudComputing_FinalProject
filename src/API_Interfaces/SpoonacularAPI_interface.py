from src.API_Interfaces.iAPI_interface import iAPI_interface
import json
import http.client

class SpoonacularAPI_interface(iAPI_interface):
    
    def __init__(self):
        self._get_API_key_from_envLocal("SPOONACULAR_API_KEY")
        self.conn = http.client.HTTPSConnection("api.spoonacular.com",
                                                timeout=10)
    
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
    
    def postGlycemicLoadFromIngredientList(self, ingredients: list[str]):
        """This method gets the glycemic load of a list of ingredients

        Args:
            ingredients (list[str]): List of ingredients

        Returns:
            tuple: Request code, returned data
        """
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        body = {
            "ingredients": ingredients
        }
        
        params = {
            "language": "en"
        }

        code, jsonPlain = self._apiRequest("/food/ingredients/glycemicLoad", "POST", params=params, 
                                           body=body, headers=headers)
        ret = json.loads(jsonPlain) # convert response to dict (could be modeled if necessary)

        return code, ret
    
    def getBulkInformationFromRecipeId(self, recipe_id: int):
        """This method gets the bulk information of a recipe

        Args:
            recipe_id (int): Recipe ID

        Returns:
            tuple: Request code, returned data
        """

        headers = {
            'Content-Type': 'application/json'
        }
        
        params = {
            "ids": recipe_id,
            "includeNutrition": True
        }

        code, jsonPlain = self._apiRequest(f"/recipes/informationBulk", "GET",
                                           headers=headers, params=params)
        ret = json.loads(jsonPlain) # convert response to dict (could be modeled if necessary)

        return code, ret