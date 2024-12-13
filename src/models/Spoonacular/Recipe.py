import json
from dataclasses import dataclass, field
from src.commons.Serializable import Serializable
from src.models.Spoonacular.Ingredient import Ingredient

@dataclass
class Recipe(Serializable):
   SpoonRecipeID:int = field(default_factory=int)
   Title:str = field(default_factory=str)
   Ingredients:list[Ingredient] = field(default_factory=list)
   Image:str = field(default_factory=str)
   GlycemicIndex:float = field(default_factory=float)
   
   @staticmethod
   def from_dict(json_data):
      allIngredients = json_data["usedIngredients"] + json_data["missedIngredients"]
      
      return Recipe(
         SpoonRecipeID=json_data["id"],
         Title=json_data["title"],
         Ingredients=[Ingredient.from_dict(ing) for ing in (allIngredients)],
         Image=json_data["image"]
      )
   
   @staticmethod
   def createSchema_database(tableName):
      return f"""
      CREATE TABLE IF NOT EXISTS {tableName} (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         SpoonRecipeID TEXT NOT NULL,
         Title TEXT NOT NULL
      )
      """
   
   def insertSchema_database(self, table_name):
      return f"""
      f"INSERT INTO {table_name} (SpoonRecipeID, Title) "
      f"VALUES ({self.SpoonRecipeID}, {self.title})"
      """
      
   @staticmethod    
   def getColumnsNames_database():
      return ["id", "SpoonRecipeID", "Title"]