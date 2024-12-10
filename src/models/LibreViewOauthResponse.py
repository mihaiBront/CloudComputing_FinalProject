from src.commons.Serializable import Serializable

from dataclasses import dataclass, field

@dataclass
class User(Serializable):
    FirstName: str = field(default_factory=str)
    LastName: str = field(default_factory=str)
    Email: str = field(default_factory=str)
    UserID: str = field(default_factory=str)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            FirstName = data['firstName'],
            LastName = data['lastName'],
            Email = data['email'],
            UserID = data['id']
        )
    
@dataclass
class AuthTicket(Serializable):
    Token:str = field(default_factory=str)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AuthTicket':
        return cls(Token = data['token'])
           

@dataclass
class LibreViewOauthResponse(Serializable):
    User: 'User' = field(default_factory='User')
    AuthTiket: 'AuthTicket' = field(default_factory='AuthTicket')
    
    @classmethod
    def from_dict(cls, data: dict) -> 'LibreViewOauthResponse':
        return cls(
            User = User().from_dict(data['user']),
            AuthTiket = AuthTicket().from_dict(data['authTicket'])
        )