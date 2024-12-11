from src.commons.Serializable import Serializable
from dataclasses import dataclass, field

@dataclass
class Ingredient(Serializable):
    SpoonIngredientID:int = field(default_factory=int)
    Name:str = field(default_factory=str)
    Amount:float = field(default_factory=float)
    Unit:str = field(default_factory=str)
    ImageURL:str = field(default_factory=str)
    
    def __str__(self):
        return f"{self.Amount} {self.Unit} {self.Name}"
    
    @classmethod
    def from_dict(cls, json_data) -> 'Ingredient':
        return cls(
            SpoonIngredientID=json_data["id"],
            Name=json_data["name"],
            Amount=json_data["amount"],
            Unit=json_data["unit"],
            ImageURL=json_data["image"]
        )