__all__ = ('Oauth2Access', )

from datetime import datetime, timedelta
from time import time as time_now

from scarletio import RichAttributeErrorBaseType

from .helpers import parse_joined_oauth2_scopes
from .preinstanced import Oauth2Scope


class Oauth2Access(RichAttributeErrorBaseType):
    """
    Represents a Discord oauth2 access object, what is returned by ``Client.activate_authorization_code`` if
    activating the authorization code went successfully.
    
    Attributes
    ----------
    access_token : `str`
        Token used for `Bearer` authorizations, when requesting OAuth2 data about the respective user.
    
    created_at : `datetime`
        The time when the access was last created or renewed.
    
    expires_after : `int`
        The time in seconds after this access expires.
    
    redirect_url : `str`
        The redirect url with what the user granted the authorization code for the oauth2 scopes for the application.
        
        Can be empty string if application's owner's access was requested.
    
    refresh_token : `str`
        The token used to renew the access token.
        
        Can be empty string if application's owner's access was requested.
    
    scopes : `None`, `tuple` of ``Oauth2Scope``
        A sequence of the scopes, which the user granted with the access token.
        
        Defaults to `None` if empty.
    """
    __slots__ = ('access_token', 'created_at', 'expires_after', 'redirect_url', 'refresh_token', 'scopes',)
    
    def __init__(self, data, redirect_url):
        """
        Creates an ``Oauth2Access``.
        
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
        self.expires_after = data['expires_in'] # default is 604800 (s) (1 week)
        self.scopes = parse_joined_oauth2_scopes(data['scope'])
        
        self.created_at = datetime.utcnow() # important for renewing
    
    
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
        self.expires_after = data['expires_in']
        self.scopes = parse_joined_oauth2_scopes(data['scope'])
    
    
    @property
    def expires_at(self):
        """
        Returns when the access expires.
        
        Returns
        -------
        expires_at : `datetime`
        """
        return self.created_at + timedelta(seconds=self.expires_after)
    
    
    def __repr__(self):
        """Returns the representation of the achievement."""
        repr_parts = ['<', self.__class__.__name__]
        
        if self.created_at.timestamp() + self.expires_after > time_now():
            state = 'active'
        else:
            state = 'expired'
        
        repr_parts.append(' ')
        repr_parts.append(state)
        
        repr_parts.append('scope count=')
        repr_parts.append(str(len(self.scopes)))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def has_scope(self, scope):
        """
        Returns whether the access has the given scope.
        
        Parameters
        ----------
        scope : ``Oauth2Scope``, `str`
            The scope to check out.
        
        Returns
        -------
        has_scope : `bool`
        
        Raises
        ------
        TypeError
            - If `scope` is neither `str`, ``Oauth2Scope``.
        """
        if isinstance(scope, Oauth2Scope):
            pass
        
        elif isinstance(scope, str):
            scope = Oauth2Scope.get(scope)
        
        else:
            raise TypeError(
                f'`scope` can be `str`, `{Oauth2Scope.__name__}`, got {scope.__class__.__name__}; {scope!r}.'
            )
        
        scopes = self.scopes
        if scopes is None:
            return False
        
        return (scope in scopes)
