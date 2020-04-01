# -*- coding: utf-8 -*-
__all__ = ('AO2Access', 'UserOA2', 'parse_oauth2_redirect_url')

import re
from datetime import datetime
from time import time as time_now

from .integration import Integration
from .others import PremiumType
from .user import UserBase, UserFlag

DEFAULT_LOCALE='en-US'
LOCALES={DEFAULT_LOCALE:DEFAULT_LOCALE}

def parse_locale(data):
    try:
        locale=data['locale']
    except KeyError:
        return DEFAULT_LOCALE
    
    try:
        locale=LOCALES[locale]
    except KeyError:
        LOCALES[locale]=locale
    
    return locale

def parse_preferred_locale(data):
    try:
        locale=data['preferred_locale']
    except KeyError:
        return DEFAULT_LOCALE
        
    try:
        locale=LOCALES[locale]
    except KeyError:
        LOCALES[locale]=locale

    return locale

def parse_locale_optional(data):
    try:
        locale=data['locale']
    except KeyError:
        return None
    
    try:
        locale=LOCALES[locale]
    except KeyError:
        LOCALES[locale]=locale
    
    return locale

OA2_RU_RP=re.compile('(https{0,1}://.+?)\?code=([a-zA-Z0-9]{30})')

def parse_oauth2_redirect_url(url):
    result=OA2_RU_RP.fullmatch(url)
    if result is None:
        return None
    return result.groups()

class Connection(object):
    __slots__=('friend_sync', 'id', 'integrations', 'name', 'revoked',
        'show_activity', 'type', 'verified', 'visibility',)
    def __init__(self,data):
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
            integrations=None
        else:
            if integration_datas:
                integrations=[Integration(integration_data) for integration_data in integration_datas]
            else:
                integrations=None
        self.integrations=integrations


SCOPES={v:v for v in ('activities.read', 'activities.write',
    'applications.builds.read', 'applications.builds.upload',
    'applications.entitlements', 'applications.store.update', 'bot',
    'connections', 'email', 'guilds', 'guilds.join', 'identify',
    'messages.read', 'rpc', 'rpc.api', 'rpc.notifications.read',
    'webhook.incoming')}
#Discord bug : 'activities.read'  cannot be granted
#Discord bug : 'activities.write' cannot be granted
#Discord bug : 'applications.builds.upload' cannot be granted
#rest of scopes is ignorable

class AO2Access(object):
    TOKEN_TYPE='Bearer'
    
    __slots__=('access_token', 'created_at', 'expires_in', 'redirect_url',
        'refresh_token', 'scopes',)
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
    __slots__ = ('access', 'email', 'flags', 'locale', 'mfa', 'premium_type',
    'system', 'verified',) #oauth 2 provided by scope

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
        self.flags          = UserFlag(data.get('flags',0))
        self.premium_type   = PremiumType.INSTANCES[data.get('premium_type',0)]
        self.locale         = parse_locale(data)
        self.system         = data.get('system',False)
        
    @property
    def access_token(self):
        return self.access.access_token

    @property
    def partial(self):
        return False

    @property
    def is_bot(self):
        return False

del UserBase, re
