from unittest import TestCase
from src.apiInterfaces.spoonacularAPI_interface import spoonacularAPI_interface
from src.apiInterfaces.edamemAPI_interface import edamamAPI_interface
import http.client
import json

import logging as log

class spoonacularApiTests(TestCase):
    spoon = spoonacularAPI_interface()
    
    def test_getListOfRecipesFromCorrectList(self):
        self.spoon = spoonacularAPI_interface()
        code, response = self.spoon.getRecipiesFromIngredientsList(["milk", "cocoa"], 1)
        self.assertEqual(code, 200)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        
    def test_getListOfRecipesFails_dueToInvalidApi(self):
        self.spoon = spoonacularAPI_interface()
        self.spoon._API_KEY = "invalid"
        code, response = self.spoon.getRecipiesFromIngredientsList(["milk", "cocoa"], 1)
        self.assertNotEqual(code, 200) # code 401 non valid api key
        self.assertIsInstance(response, dict) # error
        
class edamamApiTests(TestCase):
    edamam = edamamAPI_interface()
    
    recipeName = "Fresh Ham Roasted With Rye Bread and Dried Fruit Stuffing",
    ingr = [
                "1 fresh ham, about 18 pounds, prepared by your butcher (See Step 1)",
                "7 cloves garlic, minced",
                "1 tablespoon caraway seeds, crushed",
                "4 teaspoons salt",
                "Freshly ground pepper to taste",
                "1 teaspoon olive oil",
                "1 medium onion, peeled and chopped",
                "3 cups sourdough rye bread, cut into 1/2-inch cubes",
                "1 1/4 cups coarsely chopped pitted prunes",
                "1 1/4 cups coarsely chopped dried apricots",
                "1 large apple tart, peeled, cored and cut into 1/2-inch cubes",
                "2 teaspoons chopped fresh rosemary",
                "1 egg, lightly beaten",
                "1 cup chicken brother, homemade or low-sodium canned"
            ]
    
    def test_gtetNutritionalTableFromIngredients(self):
        self.edamam = edamamAPI_interface()
        
        code, response = self.edamam.gtetNutritionalTableFromIngredients(
            self.recipeName,
            self.ingr)
        self.assertEqual(code, 200)
        
    def test_gtetNutritionalTable_failsBadApi(self):
        self.edamam = edamamAPI_interface()
        
        self.edamam._APP_ID = "invalid"
        code, response = self.edamam.gtetNutritionalTableFromIngredients(
            self.recipeName,
            self.ingr)
        self.assertNotEqual(code, 200) # code 401 non valid api key
    
    def test_gtetNutritionalTable_failsBadAppName(self):
        self.edamam = edamamAPI_interface()
        
        self.edamam._APP_ID = "invalid"
        code, response = self.edamam.gtetNutritionalTableFromIngredients(
            self.recipeName,
            self.ingr)
        self.assertNotEqual(code, 200) # code 401 non valid api key
        self.assertIsInstance(response, dict) # error
        
class spoonEdamamIntegrationTests(TestCase):
    def test_getListOfRecipesFromCorrectList(self):
        pass