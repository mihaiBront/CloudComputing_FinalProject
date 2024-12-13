from src.commons.FileManagement import FileManagement
from src.models.Spoonacular.Recipe import Recipe
from src.models.LibreView.Glucose.Period import Period

import sqlite3
from dataclasses import dataclass, field
import os
import logging as log

@dataclass
class DataBase(object):
    Path:str = field(default_factory=str)
    TablesSchema: list[dict] = field(default_factory=list)
    Connection: sqlite3.Connection | None = None
    Cursor: sqlite3.Cursor | None = None
    
    def _createOrConnect(self):
        if not os.path.exists(self.Path):
            log.info(f"Creating database at {self.Path}")
            FileManagement.create_dir_if_not_exists(self.Path)
        
        log.info(f"Connecting to database at {self.Path}")
        self.Connection = sqlite3.connect(self.Path)
        self.Cursor = self.Connection.cursor()
        
        self._init_tables()
    
    def _init_tables(self):
        log.info("Initializing tables")
        
        #create recipes table
        self.Cursor.execute(Recipe.createSchema_database("recipes"))
        self.Connection.commit()

        #create glucose historic periods table
        self.Cursor.execute(Period.createSchema_database("glucose_periods"))
        self.Connection.commit()
        
        return

#region recipe table methods
    def insertRecipe(self, recipe:Recipe):
        self.Cursor.execute(recipe.insertSchema_database("recipes"))
        self.Connection.commit()

        return
    
    def getRecipesList(self):
        self.Cursor.execute("SELECT * FROM recipes")
        recipes = self.Cursor.fetchmany(20)
        return recipes
    
    def deleteRecipe(self, recipe_id):
        self.Cursor.execute(f"DELETE FROM recipes WHERE id = {recipe_id}")
        self.Connection.commit()
        return
#endregion

#region glucose periods table methods
    def insertPeriod(self, period:Period):
        self.Cursor.execute(period.insertSchema_database("glucose_periods"))
        self.Connection.commit()
        return

    def getPeriodsList(self):
        self.Cursor.execute("SELECT * FROM glucose_periods")
        periods = self.Cursor.fetchmany(20)
        return periods

    def deletePeriod(self, period_id):
        self.Cursor.execute(f"DELETE FROM glucose_periods WHERE id = {period_id}")
        self.Connection.commit()
        return
#endregion