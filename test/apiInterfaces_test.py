from unittest import TestCase

from src.API_Interfaces.SpoonacularAPI_interface import SpoonacularAPI_interface
from src.API_Interfaces.LibreViewAPI_interface import LibreViewAPI_interface
from src.models.LibreView.OauthResponse import OauthResponse
from src.models.Spoonacular.RecipeProceedure import RecipeProceedure
from src.models.Spoonacular.Recipe import Recipe
from src.models.LibreView.Glucose.GlucoseReadings import GlucoseReadings
from src.commons.FileManagement import FileManagement

import os
from dotenv import load_dotenv
import json
import plotly
import pandas as pd

import logging as log
from src.commons.LoggerInitializer import LoggerInitializer
LoggerInitializer(log.INFO, "tests.log")

TEST_API_SENSITIVE = False

class spoonacularApiTests(TestCase):
    spoon = SpoonacularAPI_interface()
    
    def test_getListOfRecipesFromCorrectList(self):
        self.spoon = SpoonacularAPI_interface()
        try:
            code, response = self.spoon.getRecipiesFromIngredientsList(["milk", "cocoa"], 1)
            self.assertEqual(code, 200)
            self.assertIsInstance(response, list)
            self.assertIsInstance(response[0], dict)
            
            pathJson = ".test_resources/dumpSpoonacular/recipeList.json"
            FileManagement.create_dir_if_not_exists(pathJson)
            with open(pathJson, "w") as f:
                f.write(json.dumps(response))
            
            log.info(f"SUCCESS {response}")
        except Exception as e:
            log.error(e)
            self.assertFalse(True, f"Test failed ({e})")
            
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
        
    def test_getBulkGlycemicLoadFromIngredientsList(self):
        self.spoon = SpoonacularAPI_interface()
        try:
            code, response = self.spoon.getBulkInformationFromRecipeId(632955)
            self.assertEqual(code, 200)
            log.info(f"SUCCESS {response}")
        except Exception as e:
            log.error(e)
            self.assertFalse(True, "Test failed {e}")
            
        try:
            recipeProceedure = RecipeProceedure.from_dict(response[0])
            self.assertIsInstance(recipeProceedure, RecipeProceedure)

            string = recipeProceedure.to_dict()
            
            log.info(f"SUCCESS {recipeProceedure}")
        
        except Exception as e:
            log.error(e)
            self.assertFalse(True, f"Test failed serializing /deserializing {e}")

class libreViewApiTests(TestCase):
    def testConstruct(self):
        libreApi = LibreViewAPI_interface()
        self.assertIsInstance(libreApi, LibreViewAPI_interface)
        
        print(libreApi._PatientId)
        print(libreApi._ACCOUNT_ID)
        
        self.assertIsNotNone(libreApi._API_KEY)
        self.assertIsNotNone(libreApi._PatientId)

    def test_oAuthRequest(self):
        jsonFilePath = ".test_resources/oauth_emailAndPassword.json"
        if not os.path.isfile(jsonFilePath):
            log.warning(f"Test not applicable; {jsonFilePath} does not exist")
            return
        
        if not TEST_API_SENSITIVE:
            log.warning(f"Test not applicable; TEST_API_SENSITIVE is False")
            return
        
        # arrange: read json from files
        with open(jsonFilePath, "r") as f:
            oauth_json = f.read()
        
        oauth_json = json.loads(oauth_json)
        
        oAuth = LibreViewAPI_interface()
        
        oAuth.oAuth(oauth_json["email"], oauth_json["password"])
        self.assertIsNotNone(oAuth._API_KEY)
    
    def test_getLastWeeksData(self):
        libreApi = LibreViewAPI_interface()

        code, data = libreApi.getLastWeekMeasurement(1,7)
        
        self.assertEqual(code, 200)
        
        try:
            gr: GlucoseReadings = GlucoseReadings.from_dict(data)
            self.assertIsInstance(gr, GlucoseReadings)
            self.assertIsNotNone(gr.Periods)
            self.assertGreater(len(gr.Periods), 0)
            
            if len(gr.Periods) > 0:
                gr.to_excels(".test_resources/dumpedPeriods")
            
        except Exception as e:
            log.error(e)
            self.assertFalse(True, f"Test failed due to exception ({e})")
            
    
    def test_simulateTodaysData(self):
        libreApi = LibreViewAPI_interface()

        code, data = libreApi.simulateGettingRealTimeMeasurements()

        self.assertEqual(code, 200)
        self.assertIsInstance(data, dict)
        self.assertIsNotNone(data['time'])
        self.assertGreater(len(data['time']), 0)
        self.assertIsNotNone(data['glucose'])
        self.assertGreater(len(data['glucose']), 0)
        
        _dir = ".test_resources/dumpGraph/test_synthetic.html"
        FileManagement.create_dir_if_not_exists(_dir)
        
        # save data as csv
        pd.DataFrame(data).to_csv(_dir.replace(".html", ".csv"))
                
        # make graph for visual evaluation        
        fig = plotly.graph_objects.Figure()
        fig.add_trace(plotly.graph_objects.Scatter(
            x=data['time'],
            y=data['glucose'],
            mode='lines+markers',
            name='Glucose Levels'
        ))
        
        fig.update_layout(
            title='Glucose Levels Over Time',
            xaxis_title='Time',
            yaxis_title='Glucose Level',
            xaxis=dict(
                # type='date',  # Ensure the axis is treated as datetime
                # showgrid=True,  # Optional: adds grid lines for clarity
                range=[min(data['time']), max(data['time'])]
            )
        )
        
        # fig.show()
        fig.write_html(_dir)
        