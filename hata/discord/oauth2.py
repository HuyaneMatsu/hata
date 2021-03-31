# -*- coding: utf-8 -*-
__all__ = ('Achievement', 'OA2Access', 'UserOA2', 'parse_oauth2_redirect_url')

import re
from datetime import datetime
from time import time as time_now

from .bases import DiscordEntity, IconSlot
from .http import URLS
from .integration import Integration
from .utils import DATETIME_FORMAT_CODE
from .user import UserBase, UserFlag
from .preinstanced import PremiumType

DEFAULT_LOCALE = 'en-US'
LOCALES = {DEFAULT_LOCALE: DEFAULT_LOCALE}

def parse_locale(data):
    """
    Gets `'local'`'s value out from the given `dict`. If found returns it, if not, then returns `DEFAULT_LOCAL`.
    
    To not keep using new local values at every case, the already used local values are cached at `LOCALE`.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Some data received from Discord.
    
    Returns
    -------
    locale : `str`
    """
    try:
        locale = data['locale']
    except KeyError:
        return DEFAULT_LOCALE
    
    locale = LOCALES.setdefault(locale, locale)
    return locale

def parse_preferred_locale(data):
    """
    Gets `'preferred_locale'`'s value out from the given `dict`. If found returns it, if not, then returns `DEFAULT_LOCAL`.
    
    To not keep using new local values at every case, the already used local values are cached at `LOCALE`.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Some data received from Discord.
    
    Returns
    -------
    locale : `str`
    """
    try:
        locale = data['preferred_locale']
    except KeyError:
        return DEFAULT_LOCALE
    
    locale = LOCALES.setdefault(locale, locale)
    return locale

def parse_locale_optional(data):
    """
    Gets `'local'`'s value out from the given `dict`. If found returns it, if not, then returns `None`.
    
    To not keep using new local values at every case, the already used local values are cached at `LOCALE`.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Some data received from Discord.
    
    Returns
    -------
    locale : `str` or `None`
    """
    try:
        locale = data['locale']
    except KeyError:
        return None
    
    locale = LOCALES.setdefault(locale, locale)
    return locale

OA2_RU_RP = re.compile('(https?://.+?)\?code=([a-zA-Z0-9]{30})')

def parse_oauth2_redirect_url(url):
    """
    Parses the `redirect_url` and the `code` out from a whole `url`, what an user was redirected to after oauth2
    authorization.
    
    If the parsing was successful, then returns a `tuple` of `redirect_url` and `code`. If it fails, returns `None`.
    
    Parameters
    ----------
    url : `str`
        A whole to url to parse from

    Returns
    -------
    result : `None` or `tuple` (`str`, `str`)
    """
    result = OA2_RU_RP.fullmatch(url)
    if result is None:
        return None
    
    return result.groups()

class Connection(DiscordEntity):
    """
    A connection object that a user is attached to.
    
    Attributes
    ----------
    id : `int`
        The unique identifier value of the connection.
    friend_sync : `bool`
        Whether the user has friend sync enabled for the connection.
    integrations : `None` or (`list` of ``Integration``)
        A list (if any) of guild integrations which are attached to the connection.
    name : `str`
        The username of the connected account.
    revoked : `bool`
        Whether the connection is revoked.
    show_activity : `bool`
        Whether activity related to this connection will be shown in presence updates.
    type : `str`
        The service of the connection. (Like `'twitch'` or `'youtube'`.)
    verified : `bool`
        Whether the connection is verified.
    visibility : `int`
        For who is the connection visible for.
        
        Possible visibility values
        +-------+-------------------------------+
        | value | description                   |
        +=======+===============================+
        | 0     | Visible only for the user.    |
        +-------+-------------------------------+
        | 1     | Visible to everyone.          |
        +-------+-------------------------------+
    """
    __slots__ = ('friend_sync', 'integrations', 'name', 'revoked', 'show_activity', 'type', 'verified', 'visibility',)
    
    def __init__(self, data):
        """
        Creates a connection object from received connection data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`)
            Received connection data.
        """
        self.name = data['name']
        self.type = data['type']
        self.id = int(data['id'])
        self.revoked = data.get('revoked', False)
        self.verified = data.get('verified', False)
        self.show_activity = data.get('show_activity', False)
        self.friend_sync = data.get('friend_sync', False)
        self.visibility = data.get('visibility', 0)
        
        try:
            integration_datas = data['integrations']
        except KeyError:
            integrations = None
        else:
            if integration_datas:
                integrations = [Integration(integration_data) for integration_data in integration_datas]
            else:
                integrations = None
        self.integrations = integrations


SCOPES = {v: v for v in ('activities.read', 'activities.write', 'applications.builds.read',
    'applications.builds.upload', 'applications.commands', 'applications.entitlements', 'applications.store.update',
    'bot', 'connections', 'email', 'guilds', 'guilds.join', 'identify', 'messages.read', 'rpc', 'rpc.api',
    'rpc.notifications.read', 'webhook.incoming')}

# rest of scopes are ignorable

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
        A list of the scopes, what the user granted with the access token.
    
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
            try:
                scopes.add(SCOPES[scope])
            except KeyError:
                pass
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
                scopes.add(SCOPES[scope])
            except KeyError:
                pass
    
    def __repr__(self):
        """Returns the representation of the achievement."""
        state =  'active' if (self.created_at.timestamp()+self.expires_in > time_now()) else 'expired'
        return (f'<{self.__class__.__name__} {state}, access_token={self.access_token!r}, scopes count='
            f'{len(self.scopes)}>')


class UserOA2(UserBase):
    """
    Represents a Discord user with extra personal information. If a ``UserOA2`` is  created it will NOT overwrite the
    already existing user with the same ID, if exists.
    
    Attributes
    ----------

    id : `int`
        The user's unique identifier number.
    name : str
        The user's username.
    discriminator : `int`
        The user's discriminator. Given to avoid overlapping names.
    avatar_hash : `int`
        The user's avatar's hash in `uint128`.
    avatar_type : `bool`
        The user's avatar's type.
    email : `None` or `str`
        The user's email. Defaults to empty string.
    flags : ``UserFlag``
        The user's user flags.
    locale : `str`
        The preferred locale by the user.
    mfa : `bool`
        Whether the user has two factor authorization enabled on the account.
    premium_type : ``PremiumType``
        The Nitro subscription type of the user.
    system : `bool`
        Whether the user is an Official Discord System user (part of the urgent message system).
    verified : `bool`
        Whether the email of the user is verified.
    """
    __slots__ = ('access', 'email', 'flags', 'locale', 'mfa', 'premium_type', 'system', 'verified', )
    
    def __init__(self, data, access):
        self.access = access
        self.id = int(data['id'])
        self.name = data['username']
        self.discriminator = int(data['discriminator'])
        
        self._set_avatar(data)
        
        self.mfa = data.get('mfa_enabled', False)
        self.verified = data.get('verified', False)
        self.email = data.get('email')
        
        try:
            flags = data['flags']
        except KeyError:
            flags = data.get('public_flags', 0)
        
        self.flags = UserFlag(flags)
        self.premium_type = PremiumType.get(data.get('premium_type', 0))
        self.locale = parse_locale(data)
        self.system = data.get('system', False)
    
    @property
    def partial(self):
        """
        Returns whether the oauth2 user object is partial.
        
        Returns
        -------
        partial : `bool` = `False`
        """
        return False
    
    @property
    def is_bot(self):
        """
        Returns whether the oauth2 user represents a bot account.
        
        Returns
        -------
        is_bot : `bool` = `False`
        """
        return False
    
    # Reflect OA2Access
    @property
    def access_token(self):
        """
        Returns the oauth2 user's access's token.
        
        Returns
        -------
        access_token : `str`
        """
        return self.access.access_token
    
    @property
    def redirect_url(self):
        """
        Returns the oauth2 user's access's redirect url.
        
        Returns
        -------
        redirect_url : `str`
        """
        return self.access.redirect_url
    
    @property
    def refresh_token(self):
        """
        Returns the oauth2 user's access's refresh token.
        
        Returns
        -------
        refresh_token : `str`
        """
        return self.access.refresh_token
    
    @property
    def scopes(self):
        """
        Returns the oauth2 user's access's scopes.
        
        Returns
        -------
        scopes : `set` of `str`
        """
        return self.access.scopes

    def _renew(self, data):
        """
        Renews the oauth2 user's access with the given data.
        
        Parameters
        ----------
        data : `None` or (`dict` of (`str`, `Any`))
            Requested access data.
        """
        self.access._renew(data)


class Achievement(DiscordEntity):
    """
    Represents a Discord achievement created at Developer portal.
    
    Attributes
    ----------
    id : `int`
        The achievement's unique identifier number.
    application_id : `int`
        The achievement's respective application's id.
    description : `str`
        The description of the achievement.
    name : `str`
        The name of the achievement.
    secret : `bool`
        Secret achievements will *not* be shown to the user until they've unlocked them.
    secure : `bool`
        Secure achievements can only be set via HTTP calls from your server, not by a game client using the SDK.
    icon_hash : `int`
        The achievement's icon's hash. Achievements always have icon.
    icon_type : ``IconType``
        The achievement's icon's type.
    """
    __slots__ = ('application_id', 'description', 'name', 'secret', 'secure',)
    
    icon = IconSlot('icon', 'icon_hash', URLS.achievement_icon_url, URLS.achievement_icon_url_as)
    
    def __init__(self, data):
        """
        Creates an achievement with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received achievement data.
        """
        self.application_id = int(data['application_id'])
        self.id = int(data['id'])
        
        self._update_no_return(data)
    
    def __repr__(self):
        """Returns the achievement's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, id={self.id}>'
    
    def __str__(self):
        """Returns the achievement's name."""
        return self.name
    
    def __format__(self,code):
        if not code:
            return self.name
        
        if code=='c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    def _update(self, data):
        """
        Updates the achievement and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Achievement data received from Discord.
            
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------+
        | Keys          | Values    |
        +===============+===========+
        | name          | `str`     |
        +---------------+-----------+
        | description   | `str`     |
        +---------------+-----------+
        | secret        | `bool`    |
        +---------------+-----------+
        | secure        | `bool`    |
        +---------------+-----------+
        | icon          | ``Icon``  |
        +---------------+-----------+
        """
        old_attributes = {}
        
        name = data['name']['default']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        description = data['description']['default']
        if self.description != description:
            old_attributes['description'] = self.description
            self.description = description
        
        secret = data['secret']
        if self.secret != secret:
            old_attributes['secret'] = self.secret
            self.secret = secret
        
        secure = data['secure']
        if self.secure != secure:
            old_attributes['secure'] = self.secure
            self.secure = secure
        
        self._update_icon(data, old_attributes)
        
        return old_attributes
    
    def _update_no_return(self, data):
        """
        Updates the achievement with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Achievement data received from Discord.
        """
        self.name = data['name']['default']
        self.description = data['description']['default']
        
        self.secret = data['secret']
        self.secure = data['secure']
        
        self._set_icon(data)
