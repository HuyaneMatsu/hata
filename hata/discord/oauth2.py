# -*- coding: utf-8 -*-
__all__ = ('Achievement', 'AO2Access', 'UserOA2', 'parse_oauth2_redirect_url')

import re
from datetime import datetime
from time import time as time_now

from .bases import DiscordEntity
from .http import URLS
from .integration import Integration
from .others import PremiumType
from .user import UserBase, UserFlag

DEFAULT_LOCALE='en-US'
LOCALES={DEFAULT_LOCALE:DEFAULT_LOCALE}

def parse_locale(data):
    '''
    Gets `'local'`'s value out from the given `dict`. If found returns it, if not, then returns `DEFAULT_LOCAL`.
    
    To not keep using new local values at every case, the already used local values are cached at `LOCALE`.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Some data received from Discord.
    
    Returns
    -------
    locale : `str`
    '''
    try:
        locale=data['locale']
    except KeyError:
        return DEFAULT_LOCALE
    
    locale = LOCALES.setdefault(locale, locale)
    return locale

def parse_preferred_locale(data):
    '''
    Gets `'preferred_locale'`'s value out from the given `dict`. If found returns it, if not, then returns `DEFAULT_LOCAL`.
    
    To not keep using new local values at every case, the already used local values are cached at `LOCALE`.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Some data received from Discord.
    
    Returns
    -------
    locale : `str`
    '''
    try:
        locale=data['preferred_locale']
    except KeyError:
        return DEFAULT_LOCALE
    
    locale = LOCALES.setdefault(locale, locale)
    return locale

def parse_locale_optional(data):
    '''
    Gets `'local'`'s value out from the given `dict`. If found returns it, if not, then returns `None`.
    
    To not keep using new local values at every case, the already used local values are cached at `LOCALE`.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Some data received from Discord.
    
    Returns
    -------
    locale : `str` or `None`
    '''
    try:
        locale=data['locale']
    except KeyError:
        return None
    
    locale = LOCALES.setdefault(locale, locale)
    return locale

OA2_RU_RP=re.compile('(https?://.+?)\?code=([a-zA-Z0-9]{30})')

def parse_oauth2_redirect_url(url):
    """
    Parses the `redirect_url` and the `code` out from a whole `url`, what an user was redircted to after outh2 authorization.
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
        The unique identificator value of the connection.
    friend_sync : `bool`
        Whether the user has friend sync enabled for the connection.
    integrations : `None` or (`list` of ``Integration``)
        A list (if any) of guild inegrations which are attached to the connection.
    name : `str`
        The username of teh connected account.
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
        +======+===========================+
        | 0     | Visible only for the user.    |
        +-------+-------------------------------+
        | 1     | Visible to everyone.          |
        +-------+-------------------------------+
    """
    __slots__ = ('friend_sync', 'integrations', 'name', 'revoked', 'show_activity', 'type', 'verified', 'visibility',)
    
    def __init__(self, data):
        """
        Creates a connection obejct from received conenction data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`)
            Received connection data.
        """
        self.name=data['name']
        self.type=data['type']
        self.id=data['id']
        self.revoked=data.get('revoked',False)
        self.verified=data.get('verified',False)
        self.show_activity=data.get('show_activity',False)
        self.friend_sync=data.get('friend_sync',False)
        self.visibility=data.get('visibility',0)
        
        try:
            integration_datas=data['integrations']
        except KeyError:
            integrations = None
        else:
            if integration_datas:
                integrations = [Integration(integration_data) for integration_data in integration_datas]
            else:
                integrations = None
        self.integrations=integrations


SCOPES={v:v for v in ('activities.read', 'activities.write', 'applications.builds.read', 'applications.builds.upload',
    'applications.entitlements', 'applications.store.update', 'bot', 'connections', 'email', 'guilds', 'guilds.join',
    'identify', 'messages.read', 'rpc', 'rpc.api', 'rpc.notifications.read', 'webhook.incoming')}
# rest of scopes is ignorable

class AO2Access(object):
    TOKEN_TYPE='Bearer'
    
    __slots__ = ('access_token', 'created_at', 'expires_in', 'redirect_url', 'refresh_token', 'scopes',)
    def __init__(self,data,redirect_url):
        self.redirect_url=redirect_url
        self.access_token=data['access_token']
        self.refresh_token=data.get('refresh_token','')
        self.expires_in=data['expires_in'] #default is 604800 (s) (1 week)
        self.scopes=scopes=set()
        for scope in data['scope'].split():
            try:
                scopes.add(SCOPES[scope])
            except KeyError:
                pass
        self.created_at=datetime.now() #important for renewing
        
    def _renew(self,data):
        self.created_at=datetime.now()
        if data is None:
            return
        self.access_token=data['access_token']
        self.refresh_token=data.get('refresh_token','')
        self.expires_in=data['expires_in']
        scopes=self.scopes
        scopes.clear()
        for scope in data['scope'].split():
            try:
                scopes.add(SCOPES[scope])
            except KeyError:
                pass
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {"active" if (self.created_at.timestamp()+self.expires_in > time_now()) else "expired"}, access_token={self.access_token!r}, scopes count={len(self.scopes)}>'
        
        
class UserOA2(UserBase):
    __slots__ = ('access', 'email', 'flags', 'locale', 'mfa', 'premium_type', 'system', 'verified', )

    def __init__(self,data,access):
        self.access         = access
        self.id             = int(data['id'])
        self.name           = data['username']
        self.discriminator  = int(data['discriminator'])

        avatar=data.get('avatar')
        if avatar is None:
            self.avatar     = 0
            self.has_animated_avatar=False
        elif avatar.startswith('a_'):
            self.avatar     = int(avatar[2:],16)
            self.has_animated_avatar=True
        else:
            self.avatar     = int(avatar,16)
            self.has_animated_avatar=False

        self.mfa            = data.get('mfa_enabled',False)
        self.verified       = data.get('verified',False)
        self.email          = data.get('email','')
        
        try:
            flags = data['flags']
        except KeyError:
            flags = data.get('public_flags',0)
        
        self.flags          = UserFlag(flags)
        self.premium_type   = PremiumType.INSTANCES[data.get('premium_type',0)]
        self.locale         = parse_locale(data)
        self.system         = data.get('system',False)
    
    @property
    def partial(self):
        return False
    
    @property
    def is_bot(self):
        return False
    
    # Reflect AO2Access
    @property
    def access_token(self):
        return self.access.access_token
    
    @property
    def redirect_url(self):
        return self.access.redirect_url
    
    @property
    def refresh_token(self):
        return self.access.refresh_token
    
    @property
    def scopes(self):
        return self.access.scopes

    def _renew(self, data):
        self.access._renew(data)


class Achievement(DiscordEntity):
    __slots__ = ('application_id', 'description', 'icon', 'name', 'secret', 'secure',)
    
    def __init__(self,data):
        self.application_id=int(data['application_id'])
        self.id=int(data['id'])

        self._update_no_return(data)

    icon_url=property(URLS.achievement_icon_url)
    icon_url_as=URLS.achievement_icon_url_as
    
    def __repr__(self):
        """Returns the achievement's represnetation."""
        return f'<{self.__class__.__name__} name={self.name!r}, id={self.id}>'
    
    def __str__(self):
        """Returns the achievement's name."""
        return self.name
    
    def __format__(self,code):
        if not code:
            return self.name
        if code=='c':
            return self.created_at.__format__('%Y.%m.%d-%H:%M:%S')
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    def _update(self,data):
        old={}
        
        name=data['name']['default']
        if self.name!=name:
            old['name']=self.name
            self.name=name
        
        description=data['description']['default']
        if self.description!=description:
            old['description']=self.description
            self.description=description
        
        secret=data['secret']
        if self.secret!=secret:
            old['secret']=self.secret
            self.secret=secret
        
        secure=data['secure']
        if self.secure!=secure:
            old['secure']=self.secure
            self.secure=secure
        
        icon=data.get('icon_hash')
        icon=0 if icon is None else int(icon,16)
        if self.icon!=icon:
            old['icon']=icon
            self.icon=icon
        
        return old
    
    def _update_no_return(self,data):
        self.name=data['name']['default']
        self.description=data['description']['default']
        
        self.secret=data['secret']
        self.secure=data['secure']
        
        icon=data.get('icon_hash')
        self.icon=0 if icon is None else int(icon,16)

del UserBase
del re
del URLS
del DiscordEntity
