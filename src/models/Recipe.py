import json
from dataclasses import dataclass, field
from src.models.Ingredient import Ingredient

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