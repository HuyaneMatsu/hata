__all__ = ('Oauth2Access', )

from datetime import datetime as DateTime, timedelta as TimeDelta
from time import time as time_now

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_access_token, parse_expires_after, parse_refresh_token, parse_scopes, put_access_token_into,
    put_expires_after_into, put_refresh_token_into, put_scopes_into, validate_access_token, validate_created_at,
    validate_expires_after, validate_redirect_url, validate_refresh_token, validate_scopes
)
from .preinstanced import Oauth2Scope


class Oauth2Access(RichAttributeErrorBaseType):
    """
    Represents a Discord oauth2 access object, what is returned by ``Client.activate_authorization_code`` if
    activating the authorization code went successfully.
    
    Attributes
    ----------
    access_token : `str`
        Token used for `Bearer` authorizations, when requesting OAuth2 data about the respective user.
    
    created_at : `DateTime`
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
    
    def __new__(
        cls,
        *,
        access_token = ...,
        created_at = ...,
        expires_after = ...,
        redirect_url = ...,
        refresh_token = ...,
        scopes = ...,
    ):
        """
        Creates a new oauth2 access with the given fields.
        
        Parameters
        ----------
        access_token : `str`, Optional (Keyword only)
            Token used for `Bearer` authorizations, when requesting OAuth2 data about the respective user.
        
        created_at : `DateTime`, Optional (Keyword only)
            The time when the access was last created or renewed.
        
        expires_after : `int`, Optional (Keyword only)
            The time in seconds after this access expires.
        
        redirect_url : `str`, Optional (Keyword only)
            The redirect url with what the user granted the authorization code for the oauth2 scopes for the application.
        
        refresh_token : `str`, Optional (Keyword only)
            The token used to renew the access token.
        
        scopes : `None`, `iterable` of (`str`, ``Oauth2Scope``), Optional (Keyword only)
            A sequence of the scopes, which the user granted with the access token.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # access_token
        if access_token is ...:
            access_token = ''
        else:
            access_token = validate_access_token(access_token)
        
        # created_at
        if created_at is ...:
            created_at = DateTime.utcnow()
        else:
            created_at = validate_created_at(created_at)
        
        # expires_after
        if expires_after is ...:
            expires_after = 604800
        else:
            expires_after = validate_expires_after(expires_after)
        
        # redirect_url
        if redirect_url is ...:
            redirect_url = ''
        else:
            redirect_url = validate_redirect_url(redirect_url)
        
        # refresh_token
        if refresh_token is ...:
            refresh_token = ''
        else:
            refresh_token = validate_refresh_token(refresh_token)
        
        # scopes
        if scopes is ...:
            scopes = None
        else:
            scopes = validate_scopes(scopes)
        
        # Construct
        self = object.__new__(cls)
        self.access_token = access_token
        self.created_at = created_at
        self.expires_after = expires_after
        self.redirect_url = redirect_url
        self.refresh_token = refresh_token
        self.scopes = scopes
        return self
    
    
    @classmethod
    def from_data(cls, data, redirect_url):
        """
        Creates an ``Oauth2Access``.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received access data.
        redirect_url : `str`
            The redirect url with what the user granted the authorization code for the oauth2 scopes for the
            application.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.access_token = parse_access_token(data)
        self.created_at = DateTime.utcnow()
        self.expires_after = parse_expires_after(data)
        self.redirect_url = redirect_url
        self.refresh_token = parse_refresh_token(data)
        self.scopes = parse_scopes(data)
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the access to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_access_token_into(self.access_token, data, defaults)
        put_expires_after_into(self.expires_after, data, defaults)
        put_refresh_token_into(self.refresh_token, data, defaults)
        put_scopes_into(self.scopes, data, defaults)
        return data
    
    
    def copy(self):
        """
        Copies the oauth2 access.
        
        Returns
        -------
        new : `instance<type<self>``
        """
        new = object.__new__(type(self))
        new.access_token = self.access_token
        new.created_at = self.created_at
        new.expires_after = self.expires_after
        new.redirect_url = self.redirect_url
        new.refresh_token = self.refresh_token
        scopes = self.scopes
        if (scopes is not None):
            scopes = (*scopes,)
        new.scopes = scopes
        return new
        
    
    def copy_with(
        self,
        *,
        access_token = ...,
        created_at = ...,
        expires_after = ...,
        redirect_url = ...,
        refresh_token = ...,
        scopes = ...,
    ):
        """
        Copies the oauth2 scopes with the given fields.
        
        Parameters
        ----------
        access_token : `str`, Optional (Keyword only)
            Token used for `Bearer` authorizations, when requesting OAuth2 data about the respective user.
        
        created_at : `DateTime`, Optional (Keyword only)
            The time when the access was last created or renewed.
        
        expires_after : `int`, Optional (Keyword only)
            The time in seconds after this access expires.
        
        redirect_url : `str`, Optional (Keyword only)
            The redirect url with what the user granted the authorization code for the oauth2 scopes for the application.
        
        refresh_token : `str`, Optional (Keyword only)
            The token used to renew the access token.
        
        scopes : `None`, `iterable` of (`str`, ``Oauth2Scope``), Optional (Keyword only)
            A sequence of the scopes, which the user granted with the access token.
        
        Returns
        -------
        new : `instance<type<self>``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # access_token
        if access_token is ...:
            access_token = self.access_token
        else:
            access_token = validate_access_token(access_token)
        
        # created_at
        if created_at is ...:
            created_at = self.created_at
        else:
            created_at = validate_created_at(created_at)
        
        # expires_after
        if expires_after is ...:
            expires_after = self.expires_after
        else:
            expires_after = validate_expires_after(expires_after)
        
        # redirect_url
        if redirect_url is ...:
            redirect_url = self.redirect_url
        else:
            redirect_url = validate_redirect_url(redirect_url)
        
        # refresh_token
        if refresh_token is ...:
            refresh_token = self.refresh_token
        else:
            refresh_token = validate_refresh_token(refresh_token)
        
        # scopes
        if scopes is ...:
            scopes = self.scopes
            if (scopes is not None):
                scopes = (*scopes,)
        else:
            scopes = validate_scopes(scopes)
        
        # Construct
        new = object.__new__(type(self))
        new.access_token = access_token
        new.created_at = created_at
        new.expires_after = expires_after
        new.redirect_url = redirect_url
        new.refresh_token = refresh_token
        new.scopes = scopes
        return new
    
    
    def _renew(self, data):
        """
        Renews the access with the given data.
        
        Parameters
        ----------
        data : `None` or (`dict` of (`str`, `object`))
            Requested access data.
        """
        self.created_at = DateTime.utcnow()
        if data is None:
            return
        
        self.access_token = parse_access_token(data)
        self.expires_after = parse_expires_after(data)
        self.refresh_token = parse_refresh_token(data)
        self.scopes = parse_scopes(data)
    
    
    @property
    def expires_at(self):
        """
        Returns when the access expires.
        
        Returns
        -------
        expires_at : `DateTime`
        """
        return self.created_at + TimeDelta(seconds = self.expires_after)
    
    
    def __repr__(self):
        """Returns the representation of the oath2 access."""
        repr_parts = ['<', self.__class__.__name__]
        
        if self.created_at.timestamp() + self.expires_after > time_now():
            state = 'active'
        else:
            state = 'expired'
        
        repr_parts.append(' ')
        repr_parts.append(state)
        
        repr_parts.append('scope count: ')
        repr_parts.append(str(len(self.scopes)))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the oauth2 scope's hash value."""
        hash_value = 0
        
        # access_token
        hash_value ^= hash(self.access_token)
        
        # created_at
        hash_value ^= hash(self.created_at)
        
        # expires_after
        hash_value ^= hash(self.expires_after)
        
        # redirect_url
        hash_value ^= hash(self.redirect_url)
        
        # refresh_token
        hash_value ^= hash(self.refresh_token)
        
        # scopes
        scopes = self.scopes
        if (scopes is not None):
            hash_value ^= len(scopes) << 22
            
            for scope in scopes:
                hash_value ^= hash(scope)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two oauth2 access are equal."""
        if type(self) is not type(other):
            return False
        
        # access_token
        if self.access_token != other.access_token:
            return False
        
        # created_at
        if self.created_at != other.created_at:
            return False
        
        # expires_after
        if self.expires_after != other.expires_after:
            return False
        
        # redirect_url
        if self.redirect_url != other.redirect_url:
            return False
        
        # refresh_token
        if self.refresh_token != other.refresh_token:
            return False
        
        # scopes
        if self.scopes != other.scopes:
            return False
        
        return True
    
    
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
    
    
    def iter_scopes(self):
        """
        Iterates over the oauth2 scopes of the oauth2 access.
        
        This method is an iterable generator.
        
        Yields
        ------
        scope : ``Oauth2Scope``
        """
        scopes = self.scopes
        if (scopes is not None):
            yield from scopes
