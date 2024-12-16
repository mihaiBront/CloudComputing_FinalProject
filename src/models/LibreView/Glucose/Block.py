from src.commons.Serializable import Serializable

import json
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Block(Serializable):
    Time: str = field(default_factory=str)
    Percentile5: float = field(default_factory=float)
    Percentile25: float = field(default_factory=float)
    Percentile50: float = field(default_factory=float)
    Percentile75: float = field(default_factory=float)
    Percentile95: float = field(default_factory=float)
    
    @classmethod
    def from_dict(cls, json_dict):
        return cls(
            Time=str(json_dict.get("time", "")),
            Percentile5=str(json_dict.get("percentile5", 0)),
            Percentile25=str(json_dict.get("percentile25", 0)),
            Percentile50=str(json_dict.get("percentile50", 0)),
            Percentile75=(json_dict.get("percentile75", 0)),
            Percentile95=(json_dict.get("percentile95", 0))
        )