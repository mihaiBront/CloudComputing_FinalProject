from src.commons.Serializable import Serializable
from src.models.LibreView.Glucose.BlockVector import BlockVector

from dataclasses import dataclass, field

@dataclass
class GData(Serializable):
    MaxGlucoseRange: int = field(default_factory=int)
    MinGlucoseRange: int = field(default_factory=int)
    MaxGlucoseValue: int = field(default_factory=int)
    Blocks: BlockVector = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, json_dict):
        return cls(
            MaxGlucoseRange=json_dict.get("maxGlucoseRange", 0),
            MinGlucoseRange=json_dict.get("minGlucoseRange", 0),
            MaxGlucoseValue=json_dict.get("maxGlucoseValue", 0),
            Blocks=BlockVector.from_dict(json_dict.get("blocks", []))
        )