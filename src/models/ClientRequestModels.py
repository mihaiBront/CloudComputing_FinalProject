from src.commons.Serializable import Serializable
from dataclasses import dataclass, field

@dataclass
class Client_RecipeRequest(Serializable):
    Ingredients: list[str] = field(default_factory=list)
    Count: int = field(default_factory=int)
    
    @classmethod
    def from_dict(cls, json_dict):
        return cls(
            Ingredients = json_dict["ingredients"],
            Count = json_dict["count"]
        )
    