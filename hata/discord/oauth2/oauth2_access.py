__all__ = ('OA2Access', )

from datetime import datetime
from time import time as time_now

from .helpers import OAUTH2_SCOPES

class OA2Access:
    """
    Represents a Discord oauth2 access object, what is returned by ``Client.activate_authorization_code`` if
    activating the authorization code went successfully.
    
    Attributes
    ----------
    access_token : `str`
        Token used for `Bearer` authorizations, when requesting OAuth2 data about the respective user.
    created_at : `datetime`
        The time when the access was last created or renewed.
    expires_in : `int`
        The time in seconds after this access expires.
    redirect_url : `str`
        The redirect url with what the user granted the authorization code for the oauth2 scopes for the application.
        
        Can be empty string if application's owner's access was requested.
    refresh_token : `str`
        The token used to renew the access token.
        
        Can be empty string if application's owner's access was requested.
    scopes : `set` of `str`
        A set of the scopes, what the user granted with the access token.
    
    Class Attributes
    ----------------
    TOKEN_TYPE : `str` = `'Bearer'`
        The access token's type.
    """
    TOKEN_TYPE = 'Bearer'
    
    __slots__ = ('access_token', 'created_at', 'expires_in', 'redirect_url', 'refresh_token', 'scopes',)
    def __init__(self, data, redirect_url):
        """
        Creates an ``OA2Access``.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received access data.
        redirect_url : `str`
            The redirect url with what the user granted the authorization code for the oauth2 scopes for the
            application.
        """
        self.redirect_url = redirect_url
        self.access_token = data['access_token']
        self.refresh_token = data.get('refresh_token', '')
        self.expires_in = data['expires_in'] # default is 604800 (s) (1 week)
        self.scopes = scopes = set()
        for scope in data['scope'].split():
            scope = OAUTH2_SCOPES.get(scope, scope)
            scopes.add(scope)
        
        self.created_at = datetime.utcnow() #important for renewing
    
    def _renew(self, data):
        """
        Renews the access with the given data.
        
        Parameters
        ----------
        data : `None` or (`dict` of (`str`, `Any`))
            Requested access data.
        """
        self.created_at = datetime.utcnow()
        if data is None:
            return
        
        self.access_token = data['access_token']
        self.refresh_token = data.get('refresh_token', '')
        self.expires_in = data['expires_in']
        scopes = self.scopes
        scopes.clear()
        for scope in data['scope'].split():
            try:
                scopes.add(OAUTH2_SCOPES[scope])
            except KeyError:
                pass
    
    def __repr__(self):
        """Returns the representation of the achievement."""
        state = 'active' if (self.created_at.timestamp()+self.expires_in > time_now()) else 'expired'
        return (f'<{self.__class__.__name__} {state}, access_token={self.access_token!r}, scopes count='
            f'{len(self.scopes)}>')
