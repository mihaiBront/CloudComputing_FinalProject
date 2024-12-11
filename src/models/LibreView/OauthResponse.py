from src.commons.Serializable import Serializable
from src.models.LibreView.User import User
from src.models.LibreView.AuthTicket import AuthTicket

from dataclasses import dataclass, field


@dataclass
class OauthResponse(Serializable):
    User: 'User' = field(default_factory='User')
    AuthTiket: 'AuthTicket' = field(default_factory='AuthTicket')
    
    @classmethod
    def from_dict(cls, data: dict) -> 'OauthResponse':
        return cls(
            User = User().from_dict(data['user']),
            AuthTiket = AuthTicket().from_dict(data['authTicket'])
        )