__all__ = ('AuthenticateResponse', 'Oauth2Application', )

from ...discord.bases import DiscordEntity, IconSlot
from ...discord.http import urls as module_urls
from ...discord.oauth2 import Oauth2Scope
from ...discord.user import User
from ...discord.utils import timestamp_to_datetime


class AuthenticateResponse:
    """
    Return object of ``RPCClient.authenticate``.
    
    Attributes
    ----------
    application : ``Oauth2Application``
        The application the user authorized to.
    expires : `datetime`
        The expiration date of the oauth2 token.
    scopes : `set` of `Oauth2Scope`
        A set of scopes, what the user granted.
    user : ``ClientUserBase``
        The authenticated user.
    """
    __slots__ = ('application', 'expires', 'scopes', 'user')
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new authenticate response instance from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Authenticate response data.
        
        Returns
        -------
        self : ``AuthenticateResponse``
        """
        user = User.from_data(data['user'])
        
        raw_scopes = data['raw_scopes']
        scopes = set()
        for scope in raw_scopes:
            scope = Oauth2Scope.get(scope)
            scopes.add(scope)
        
        expires = timestamp_to_datetime(data['date'])
        
        application = Oauth2Application.from_data(data['application'])
        
        self = object.__new__(cls)
        self.user = user
        self.scopes = scopes
        self.expires = expires
        self.application = application
        return self
    
    
    def __repr__(self):
        """Returns the authenticate representation."""
        return f'<{self.__class__.__name__} user = {self.user!r}>'


class Oauth2Application(DiscordEntity):
    """
    Application details included within ``AuthenticateResponse``.
    
    Attributes
    ----------
    description : `None`, `str`
        The application's description.
    icon_hash : `int`
        The application's icon's hash as `uint128`.
    icon_type : ``IconType``
        The application's icon's type.
    name : `str`
        The application's name.
    rpc_origins : `None`, `tuple` of `str`.
        Rpc origin urls.
    """
    icon = IconSlot('icon', 'icon',
        module_urls.application_icon_url,
        module_urls.application_icon_url_as,
        add_updater = False,
    )
    
    __slots__ = ('description', 'name', 'rpc_origins',)
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new oauth2 application instance from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application oauth2 data.
        
        Returns
        -------
        self : ``Oauth2Application``
        """
        description = data['description']
        if (description is not None) and (not description):
            description = None
        
        rpc_origins = data['rpc_origins']
        if (rpc_origins is None) or (not rpc_origins):
            rpc_origins = None
        else:
            rpc_origins.sort()
            rpc_origins = tuple(rpc_origins)
        
        name = data['name']
        self = object.__new__(cls)
        self.description = description
        self._set_icon(data)
        self.name = name
        self.rpc_origins = rpc_origins
        return self
