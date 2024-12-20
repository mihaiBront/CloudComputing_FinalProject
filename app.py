from src.API_Interfaces.SpoonacularAPI_interface import SpoonacularAPI_interface
from src.API_Interfaces.LibreViewAPI_interface import LibreViewAPI_interface
import src.models.ClientRequestModels as ClientRequestModels
from src.models.Spoonacular.Recipe import Recipe
from src.models.Spoonacular.RecipeProceedure import RecipeProceedure
from src.commons.PlotlyGraphHelper import PlotlyGraphHelper
from src.glucosePrediction.GlucosePredictor import GlucosePredictor

from flask import Flask, render_template, jsonify, request, send_from_directory
from http import HTTPStatus
from dotenv import load_dotenv, set_key
import os
import json

#---DEFINES---
DEBUG = False
    
app = Flask(__name__)

#---------------------#
#-   API ENDPOINTS   -#
#---------------------#
#region API_ENDPOINTS

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates/resources'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    """ Navigates to the index page (base route)

    Returns:
        str: Template
    """
    return render_template('index.html')

@app.route('/debug')
def debug():
    """ Navigates to the debug page

    Returns:
        str: Template
    """
    return render_template('html/debug.html')

@app.route('/login')
def recipe():
    """ Navigates to the login page

    Returns:
        str: Template
    """
    return render_template('html/login.html')

#endregion

#-------------------#
#-   API METHODS   -#
#-------------------#
#region API_METHODS   

@app.route('/getHelloWorld', methods=['POST'])
def getHelloWorld():
    """DEPRECATED: Kept for consistancy in repository
    """
    try:
        data = request.get_json()
        name = data.get('name', 'name')

        if len(name) == 0:
            raise Exception("No name provided")

        return jsonify(error="The sample method this endpoind called is no longer available"), HTTPStatus.BAD_REQUEST
    
    except Exception as ex:
        return jsonify(error=f"{ex} :´("), 500

@app.route('/getRecipes', methods=['POST'])
def getRecipes():
    """Gets recipes based on provided ingredients and count
    
    Expects a POST request with JSON payload containing:
    - Ingredients (list): List of ingredients to search recipes for
    - Count (int): Number of recipes to return
    
    Returns:
        tuple: JSON response containing:
            - recipes (list): List of Recipe objects with recipe details including:
                - Recipe ID
                - Title
                - Image URL
                - Missing ingredients count
                - Used ingredients count
                - Ingredients list
                - Glycemic load
            - HTTP status code
            
    Raises:
        HTTPStatus.BAD_REQUEST: If request payload is invalid
        HTTPStatus.INTERNAL_SERVER_ERROR: If API call fails
    """        
    try:
        #get passed json
        data = request.get_json()
        
        #make class from json (assures the request is correct; else, it is caught by exception)
        data = ClientRequestModels.Client_RecipeRequest.from_dict(data)
        
        # making api petition
        spoon = SpoonacularAPI_interface()
        code, responsedata = spoon.getRecipiesFromIngredientsList(data.Ingredients, data.Count)
        
        if DEBUG:
            if not os.path.exists(".test_resources"): os.mkdirs(".test_resources")
            with open(".test_resources/last_request_recipeList.json", "w") as f:
                f.write(json.dumps(responsedata, indent=4))
        
        if code != HTTPStatus.OK:
            return jsonify(error=f"(responsedata)"), code
        
        # construct recipes elements
        recipes = [Recipe.from_dict(recipe) for recipe in responsedata]
        
        # get glycemic index for each recipe
        for i in range(len(recipes)):
            _iList = [f"{ingredient.Amount} {ingredient.Unit} {ingredient.Name}" 
                      for ingredient in recipes[i].Ingredients]
            code, glycemicLoad = spoon.postGlycemicLoadFromIngredientList(_iList)
            
            if code != HTTPStatus.OK:
                return jsonify(error=f"(responsedata)"), code
            
            recipes[i].GlycemicLoad = glycemicLoad.get("totalGlycemicLoad", 0.0)
        
        resp = jsonify(recipes=[recipe.to_dict() for recipe in recipes])
        
        return resp, HTTPStatus.OK
    
    except Exception as ex:
        return jsonify(error=f"{ex}"), HTTPStatus.BAD_REQUEST
    
@app.route('/getRecipeInformation', methods=['POST'])
def getRecipeInformation():
    """Gets detailed recipe information for a specific recipe ID
    
    Expects a POST request with JSON payload containing:
    - spoonRecipeID (int): Spoonacular recipe ID to get details for
    
    Returns:
        tuple: JSON response containing:
            - recipe (dict): RecipeProceedure object with detailed recipe information including:
                - Recipe ID
                - Title 
                - Image URL
                - Servings
                - Ready in minutes
                - Instructions
                - Ingredients list with amounts
                - Nutrition information
            - HTTP status code
            
    Raises:
        HTTPStatus.BAD_REQUEST: If request payload is invalid
        HTTPStatus.INTERNAL_SERVER_ERROR: If API call fails
    """
    try:
        #get passed json
        data = request.get_json()

        #make class from json (assures the request is correct; else, it is caught by exception)
        data = data["spoonRecipeID"]

        # making api petition
        spoon = SpoonacularAPI_interface()
        code, responsedata = spoon.getBulkInformationFromRecipeId(data)

        if DEBUG:
            if not os.path.exists(".test_resources"): os.mkdirs(".test_resources")
            with open(".test_resources/last_request_bulk.json", "w") as f:
                f.write(json.dumps(responsedata, indent=4))

        if code != HTTPStatus.OK:
            return jsonify(error=f"(responsedata)"), code

        # construct recipes elements
        recipe = responsedata[0]
        recipe = RecipeProceedure.from_dict(recipe)

        resp = jsonify(recipe.to_dict())

        return resp, HTTPStatus.OK

    except Exception as ex:
        return jsonify(error=f"{ex}"), HTTPStatus.BAD_REQUEST
    
@app.route('/getGlucoseData', methods=['GET'])
def getGlucoseData():
    """Gets glucose readings for the last 24 hours and generates visualization
    
    Makes a GET request to retrieve glucose data and creates an interactive plot
    
    Returns:
        tuple: JSON response containing:
            - data (dict): Dictionary containing:
                - graph (str): HTML string of Plotly graph visualization showing:
                    - Historical glucose readings for last 24 hours
                    - Predicted glucose values (currently returns actual values)
                    - Graph y-axis range from 30-350 mg/dL
            - HTTP status code
            
    Raises:
        HTTPStatus.BAD_REQUEST: If request fails
        HTTPStatus.INTERNAL_SERVER_ERROR: If API call fails
    """        
    try:
        # making api petition
        libre = LibreViewAPI_interface()
        code, responsedata = libre.simulateGettingRealTimeMeasurements()

        if code != HTTPStatus.OK:
            return jsonify(error=f"(responsedata)"), code
        
        if DEBUG:
            
            htmlGraph = PlotlyGraphHelper.glucosePredictionGraphHtml(
                responsedata, responsedata, ymin = 30, ymax = 350)
            
            if not os.path.exists(".test_resources"): os.mkdirs(".test_resources")
            with open(".test_resources/last_request_graph.html", "w") as f:
                f.write(htmlGraph)
        
        for key, value in responsedata.items():
            responsedata[key] = list(value)
        
        ret = {
            "readings": responsedata,
            "prediction": responsedata
        }

        return ret, HTTPStatus.OK
        
    except Exception as ex:
        return jsonify(error=f"{ex}"), HTTPStatus.BAD_REQUEST
    
@app.route('/getGlucosePrediction', methods=['POST'])
def getGlucosePrediction():
    """Gets glucose readings for the last 24 hours and generates visualization
    
    Makes a GET request to retrieve glucose data and creates an interactive plot
    
    Returns:
        tuple: JSON response containing:
            - data (dict): Dictionary containing:
                - graph (str): HTML string of Plotly graph visualization showing:
                    - Historical glucose readings for last 24 hours
                    - Predicted glucose values (currently returns actual values)
                    - Graph y-axis range from 30-350 mg/dL
            - HTTP status code
            
    Raises:
        HTTPStatus.BAD_REQUEST: If request fails
        HTTPStatus.INTERNAL_SERVER_ERROR: If API call fails
    """        
    try:
        # get request data
        data = request.get_json()
            
        _insulin_input = float(data.get("insulin", 0))
        _carbs_input = float(data.get("carbs", 0))
        
        # making api petition for glucose data
        libre = LibreViewAPI_interface()
        code, responsedata = libre.simulateGettingRealTimeMeasurements()

        if code != HTTPStatus.OK:
            return jsonify(error=f"(responsedata)"), code

        # TODO: make prediction:
        try:            
            _model = GlucosePredictor('./reggressionGlucoseSimple.joblib')
            _model.loadModel()
            
            prediction = _model.simulatePrediction(responsedata["time"], responsedata["glucose"], _insulin_input, _carbs_input)
        except Exception as ex:
            return jsonify(error=f"Prediction failed: {ex}"), HTTPStatus.INTERNAL_SERVER_ERROR            
        
        # convert data to arrays
        for key, value in responsedata.items():
            responsedata[key] = list(value)

        for key, value in prediction.items():
            prediction[key] = list(value)[-6:]
        
        ret = {
            "readings": responsedata,
            "prediction": prediction
        }
        
        if DEBUG:
            htmlGraph = PlotlyGraphHelper.glucosePredictionGraphHtml(
                responsedata, prediction, ymin = 30, ymax = 350)
            
            with open("./.test_resources/last_request_graph_ored.html", "w") as f:
                f.write(htmlGraph)

        return ret, HTTPStatus.OK
        
    except Exception as ex:
        return jsonify(error=f"{ex}"), HTTPStatus.BAD_REQUEST

@app.route('/setApiKeys', methods=['POST'])
def setApiKeys():
    """Sets API keys for Spoonacular and LibreView

    Expects a POST request with JSON payload containing:
    - spoonacularAPIKey (str): Spoonacular API key
    - libreViewAPIKey (str): LibreView API key

    Returns:
        tuple: JSON response containing:
            - message (str): Success message
            - HTTP status code

    Raises:
        HTTPStatus.BAD_REQUEST: If request payload is invalid
        HTTPStatus.INTERNAL_SERVER_ERROR: If API call fails
    """
    try:
        #get passed json
        data = request.get_json()

        _spoonacularAPIKey = data.get('spoonacularAPIKey', '')
        _libreviewApiKey = data.get('libreViewAPIKey', '')
        _libreviewAccountId = data.get('libreViewAccountId', '')

        secretEnvPath = ".env.local"
        if not os.path.exists(secretEnvPath):
            with open(secretEnvPath, "w") as f:
                pass
        
        set_key(secretEnvPath, "SPOONACULAR_API_KEY", _spoonacularAPIKey)
        set_key(secretEnvPath, "LIBREVIEW_API_KEY", _libreviewApiKey)
        set_key(secretEnvPath, "LIBREVIEW_ACCOUNT_ID", _libreviewAccountId)
        
        return jsonify(message="API keys set successfully"), HTTPStatus.OK

    except Exception as ex:
        return jsonify(error=f"{ex}"), HTTPStatus.BAD_REQUEST
#endregion