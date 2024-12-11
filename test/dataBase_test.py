from unittest import TestCase
from src.db.DataBase import DataBase

class DataBaseTests(TestCase):
    
    def test_createDataBase(self):
        db = DataBase(Path="./.database/data.db")
        db._createAndConnect()