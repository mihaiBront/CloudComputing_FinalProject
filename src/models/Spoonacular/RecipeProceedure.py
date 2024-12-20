from src.commons.Serializable import Serializable
from src.models.Spoonacular.Ingredient import Ingredient
from dataclasses import dataclass, field
    
@dataclass
class RecipeProceedure(Serializable):
    SpoonRecipeID: int = field(default_factory=int)
    Title:str = field(default_factory=str)
    Ingredients: list[Ingredient] = field(default_factory=list)
    Image: str = field(default_factory=str)
    
    SourceURL: str = field(default_factory=str)
    
    Servings: int = field(default_factory=int)
    
    PreparationMinutes: int = field(default_factory=int)
    CookingMinutes: int = field(default_factory=int)
    ReadyInMinutes: int = field(default_factory=int)
    Nutrition: dict = field(default_factory=dict)
    
    Summary: str = field(default_factory=str)
    Instructions: list[str] = field(default_factory=list) # instructions are not always available
        
    @classmethod
    def from_dict(cls, json_dict:dict) -> 'RecipeProceedure':
        
        _nutrition=json_dict.get("nutrition", []).get("nutrients", [])
        
        _nut = {nut["name"]:nut["amount"] for nut in _nutrition}
        
        _analyzedInstructions=json_dict.get("analyzedInstructions", [])
        if len(_analyzedInstructions) > 0:
            _analyzedInstructions = _analyzedInstructions[0].get("steps", [])
        
        return cls(
            SpoonRecipeID=json_dict["id"],
            Title=json_dict["title"],
            Ingredients=[Ingredient.from_dict(ing) for ing in json_dict.get("extendedIngredients", [])],
            Image=json_dict["image"],
            
            SourceURL=json_dict["sourceUrl"],
            
            Servings=json_dict["servings"],
            
            PreparationMinutes=json_dict["preparationMinutes"],
            CookingMinutes=json_dict["cookingMinutes"],
            ReadyInMinutes=json_dict["readyInMinutes"],
            
            Nutrition=_nut,
            
            Summary=json_dict["summary"],
            Instructions=[{
                "step": step["step"], 
                "number": step["number"]
                } for step in _analyzedInstructions]
        )
