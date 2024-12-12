from unittest import TestCase
from src.db.DataBase import DataBase

class DataBaseTests(TestCase):
    db = DataBase(Path=".test_resources/database.db")
    
    def test_createDataBase(self):
        self.db._createOrConnect()
        
    def test_tablesExist(self):
        self.db._createOrConnect()
        self.assertTrue(self.db._tablesExist())
        
    