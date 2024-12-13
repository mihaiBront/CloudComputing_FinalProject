from src.models.Spoonacular.Recipe import Recipe
from src.models.LibreView.Glucose.Period import Period

from unittest import TestCase
from src.db.DataBase import DataBase

class DataBaseTests(TestCase):
    db = DataBase(path=".test_resources/database.db")
    
    def test_createDataBase(self):
        self.db = DataBase(path=".test_resources/database.db")
        
    def test_tablesExist(self):
        tables_query = """
        SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
        """

        requiredTables = ["recipes", "glucose_periods"]
        
        self.db.Cursor.execute(tables_query)
        tables = [tab[0] for tab in self.db.Cursor.fetchall()]
        tables.remove("sqlite_sequence")

        # Assert that the query returns at least one table
        self.assertTrue(len(tables) > 0, "No tables found in the database.")
        self.assertEqual(sorted(tables), sorted(requiredTables), "Tables do not match expected tables.")

        # Dictionary to hold tables and their columns
        requiredColumns = {
            "recipes": Recipe.getColumnsNames_database(),
            "glucose_periods": Period.getColumnsNames_database()
        }

        # Query to list columns for a specific table
        for table in tables:
            # extract  
            self.db.Cursor.execute(f"PRAGMA table_info({table});")
            columns = self.db.Cursor.fetchall()  # Each row contains column details
            column_names = [col[1] for col in columns]  # Extract column names
            
            self.assertEqual(sorted(column_names), sorted(requiredColumns[table]), f"Columns do not match for table '{table}'.")
    