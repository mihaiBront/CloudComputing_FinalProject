from unittest import TestCase
from src.API_Interfaces.SpoonacularAPI_interface import SpoonacularAPI_interface
from src.API_Interfaces.LibreViewAPI_interface import LibreViewOauthResponse
from src.models.LibreViewOauthResponse import LibreViewOauthResponse
from src.models.Recipe import Recipe

import os

import logging as log
from src.commons.LoggerInitializer import LoggerInitializer
LoggerInitializer(log.INFO, "tests.log")


class spoonacularApiTests(TestCase):
    spoon = SpoonacularAPI_interface()
    
    def test_getListOfRecipesFromCorrectList(self):
        self.spoon = SpoonacularAPI_interface()
        try:
            code, response = self.spoon.getRecipiesFromIngredientsList(["milk", "cocoa"], 1)
            self.assertEqual(code, 200)
            self.assertIsInstance(response, list)
            self.assertIsInstance(response[0], dict)
            log.info(f"SUCCESS {response}")
        except Exception as e:
            log.error(e)
            self.assertFalse(True, "Test failed")
            
    def test_deserializeRecipeToRecipeObject(self):
        self.spoon = SpoonacularAPI_interface()
        try:
            code, response = self.spoon.getRecipiesFromIngredientsList(["milk", "cocoa"], 1)
            self.assertEqual(code, 200)
            self.assertIsInstance(response, list)
            self.assertIsInstance(response[0], dict)
            log.info(f"SUCCESS {response}")
        except Exception as e:
            log.error(e)
            self.assertFalse(True, "Test failed")
        
        recipe_json = response[0]
        try:
            recipe_deserialized = Recipe.from_dict(recipe_json)
            self.assertIsInstance(recipe_deserialized, Recipe,  
                                  "Recipe deserialized is not a Recipe object")
        except Exception as e:
            log.error(e)
            self.assertFalse(True, "Test failed")
            
        
        
    def test_getGlycemicLoadFromIngredientsList(self):
        self.spoon = SpoonacularAPI_interface()
        try:
            code, response = self.spoon.postGlycemicLoadFromIngredientList([
                                                                                "1 kiwi",
                                                                                "2 cups rice",
                                                                                "2 glasses of water"
                                                                            ])
            self.assertEqual(code, 200)
            log.info(f"SUCCESS {response}")
        except Exception as e:
            log.error(e)
            self.assertFalse(True, "Test failed")
        

class libreViewApiTests(TestCase):
    def test_deserializeJsonOauth(self):
        jsonFilePath = ".test_resources/oauth_librelink_response.json"
        if not os.path.isfile(jsonFilePath):
            log.warning(f"Test not applicable; {jsonFilePath} does not exist")
            return
        
        # arrange: read json from files
        with open(jsonFilePath, "r") as f:
            oauth_json = f.read()
        
        # act: deserialize json
        oauth_response: LibreViewOauthResponse = LibreViewOauthResponse.deserialize(oauth_json)
        
        # assert: check the object is filled
        self.assertIsInstance(oauth_response, LibreViewOauthResponse)
        self.assertIsNotNone(oauth_response.AuthTiket)
        self.assertIsNotNone(oauth_response.User)
        log.info(f"SUCCESS object serialized correctly")
    
    def test_oAuthRequest(self):
        jsonFilePath = ".test_resources/oauth_emailAndPassword.json"
        if not os.path.isfile(jsonFilePath):
            log.warning(f"Test not applicable; {jsonFilePath} does not exist")
            return
        else:
            # pending implementation
            return
        
            