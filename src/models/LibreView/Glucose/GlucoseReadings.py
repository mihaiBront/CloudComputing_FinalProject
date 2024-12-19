from src.commons.Serializable import Serializable
from src.models.LibreView.Glucose.Period import Period
from src.commons.DateTimeHelper import DateTimeHelper
from src.commons.FileManagement import FileManagement

import json
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class GlucoseReadings(Serializable):
    LastUpload: str = field(default_factory=str)
    lastUploadCGM: str = field(default_factory=str)
    Periods: list[Period] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, json_dict):
        return cls(
            LastUpload=DateTimeHelper.dateStrFromUtcInt(
                json_dict.get("lastUpload", "")),
            lastUploadCGM=DateTimeHelper.dateStrFromUtcInt(
                json_dict.get("lastUploadCGM", "")),
            Periods=[Period.from_dict(period) for period in json_dict.get("periods", [])]
        )
        
    def to_excels(self, path_to_dir):
        """Exports glucose readings periods to individual Excel files.
        
        Args:
            path_to_dir (str): Directory path where the Excel files will be saved
            
        The method will:
        - Create the directory if it doesn't exist
        - For each period in self.Periods:
            - Create a CSV file named {period.DateStart}_glucosePeriod.csv
            - Export the period data to that file
        
        Returns:
            None
        """
        
        _dir = FileManagement.get_dir_from_filepath(path_to_dir)
        FileManagement.create_dir_if_not_exists(_dir)
        
        for period in self.Periods:
            period.to_excel(f"{_dir}/{period.DateStart}_glucosePeriod.csv")
        
        return    
    
    def simulateTodaysReadings():
        pass