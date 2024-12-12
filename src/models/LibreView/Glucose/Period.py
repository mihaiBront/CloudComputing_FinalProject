from src.commons.Serializable import Serializable
from src.db.iDatabaseCompliant import iDatabaseCompliant
from src.models.LibreView.Glucose.Data import GData
from src.commons.DateTimeHelper import DateTimeHelper

import json
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class Period(Serializable, iDatabaseCompliant):
    DateEnd: str = field(default_factory=str)
    DateStart: str = field(default_factory=str)
    NoData: bool = field(default_factory=bool)
    AvgGlucose: int = field(default_factory=int)
    DaysOfData: int = field(default_factory=int)
    Data: GData = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, json_dict):
        obj = cls(
            DateEnd=DateTimeHelper.dateStrFromUtcInt(json_dict.get("dateEnd", 0)),
            DateStart=DateTimeHelper.dateStrFromUtcInt(json_dict.get("dateStart", "")),
            NoData=json_dict.get("noData", False),
            AvgGlucose=json_dict.get("avgGlucose", 0),
            DaysOfData=json_dict.get("daysOfData", 0),
            Data=GData.from_dict(json_dict["data"])
        )
        
        obj.Data.Blocks.Time = [f"{obj.DateStart} {time}" 
                                for time in obj.Data.Blocks.Time[:]]
        
        return obj
    
    def to_excel(self, save_path):
        _dict = self.Data.Blocks.to_dict()
        df = pd.DataFrame.from_dict(_dict)
        
        df.to_csv(save_path, index=False)
        
        return
    
    def createSchema_database(self, table_name):
        return f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            DateStart TEXT NOT NULL,
            DateEnd TEXT NOT NULL,
            NoData BOOLEAN NOT NULL,
            AvgGlucose INTEGER NOT NULL,
            DaysOfData TEXT NOT NULL
        )
        """
    
    def insertSchema_database(self, table_name):
        return f"""
            f"INSERT INTO {table_name} (DateStart, DateEnd, NoData, AvgGlucose, DaysOfData) "
            f"VALUES ({self.DateStart}, {self.DateEnd}, {self.NoData}, {self.AvgGlucose}, {json.dumps(self.Data.Blocks.to_dict())})"
        """
    
    