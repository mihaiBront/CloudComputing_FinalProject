from src.commons.Serializable import Serializable

from dataclasses import dataclass, field

@dataclass
class AuthTicket(Serializable):
    Token:str = field(default_factory=str)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AuthTicket':
        return cls(Token = data['token'])
           
