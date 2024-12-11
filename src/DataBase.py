import sqlite3
from dataclasses import dataclass, field

@dataclass
class DataBase(object):
    Path:str = field(default_factory=str)
    
    def createAndConnect(self):
        pass
