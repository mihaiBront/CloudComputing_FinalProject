from src.commons.Serializable import Serializable
from src.commons.DateTimeHelper import DateTimeHelper

import logging as log
import numpy as np
from dataclasses import dataclass, field
import json

@dataclass
class BlockVector(Serializable):
    Time: list[str] = field(default_factory=list)
    Percentile5: np.ndarray = field(default_factory=np.ndarray)
    Percentile25: np.ndarray = field(default_factory=np.ndarray)
    Percentile50: np.ndarray = field(default_factory=np.ndarray)
    Percentile75: np.ndarray = field(default_factory=np.ndarray)
    Percentile95: np.ndarray = field(default_factory=np.ndarray)
    
    @classmethod
    def from_dict(cls, json_dict):
        if len(json_dict) < 1:
            log.warning("Empty BlockVector")
            return cls()
        
        try:
            json_dict[0]["time"] # if all entries fit in one list
            blocks = json_dict 
        except:
            blocks = [] # make one single list if they didn't
            for lst in range(len(json_dict)):
                blocks.extend(json_dict[lst])
            
        
        _time = np.array([block["time"] for block in blocks])
        _time = [DateTimeHelper.hourFromDaysecondsInt(dayseconds) 
                 for dayseconds in _time[:]]
        
        return cls(
                Time=_time,
                Percentile5=np.array([block["percentile5"] for block in blocks]),
                Percentile25=np.array([block["percentile25"] for block in blocks]),
                Percentile50=np.array([block["percentile50"] for block in blocks]),
                Percentile75=np.array([block["percentile75"] for block in blocks]),
                Percentile95=np.array([block["percentile95"] for block in blocks]),
            )