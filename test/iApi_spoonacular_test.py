from unittest import TestCase
from src.apiInterfaces.spoonacularAPI_interface import spoonacularAPI_interface

import logging as log

class spoonacularApiTests(TestCase):
    spoon = spoonacularAPI_interface()
    
    def test_getListOfRecipesFromCorrectList(self):
        code, response = self.spoon.getRecipiesFromIngredientsList(["milk", "cocoa"], 1)
        self.assertEqual(code, 200)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        
    def test_getListOfRecipesFails_dueToInvalidApi(self):
        self.spoon._API_KEY = "invalid"
        code, response = self.spoon.getRecipiesFromIngredientsList(["milk", "cocoa"], 1)
        self.assertNotEqual(code, 200) # code 401 non valid api key
        self.assertIsInstance(response, dict) # error