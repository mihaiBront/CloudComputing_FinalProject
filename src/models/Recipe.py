import json
from dataclasses import dataclass, field
from src.models.Ingredient import Ingredient

# {
#     "id": 700339,
#     "title": "Cinnamon Vanilla Hot Chocolate",
#     "image": "https://img.spoonacular.com/recipes/700339-312x231.jpg",
#     "imageType": "jpg",
#     "usedIngredientCount": 2,
#     "missedIngredientCount": 2,
#     "missedIngredients": [
#         {
#             "id": 1012010,
#             "amount": 0.25,
#             "unit": "teaspoon",
#             "unitLong": "teaspoons",
#             "unitShort": "tsp",
#             "aisle": "Spices and Seasonings",
#             "name": "ground cinnamon",
#             "original": "¼ teaspoon ground cinnamon",
#             "originalName": "ground cinnamon",
#             "meta": [
#             ],
#             "image": "https://img.spoonacular.com/ingredients_100x100/cinnamon.jpg"
#         },
#     ],
#     "usedIngredients": [
#     ],
#     "unusedIngredients": [
#     ],
#     "likes": 0
# }

@dataclass
class Recipe(object):
   SpoonRecipeID:int = field(default_factory=int)
   Title:str = field(default_factory=str)
   Ingredients:list[Ingredient] = field(default_factory=list)
   Image:str = field(default_factory=str)
   
   def from_dict(json_data):
      return Recipe(
         SpoonRecipeID=json_data["id"],
         Title=json_data["title"],
         Ingredients=[Ingredient.from_dict(ing) for ing in (json_data["usedIngredients"]+json_data["missedIngredients"])],
         Image=json_data["image"]
      )
      
   def toEdamam(self):
      pass