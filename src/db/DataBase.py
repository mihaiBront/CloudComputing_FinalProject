from src.commons.FileManagement import FileManagement
from src.models.Spoonacular.Recipe import Recipe
from src.models.LibreView.User import User

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
    
    def _createAndConnect(self):
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

        #TODO: create glucose hystoric table
        
        return
