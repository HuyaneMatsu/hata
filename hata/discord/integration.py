# -*- coding: utf-8 -*-
__all__ = ('Integration', 'IntegrationAccount', 'IntegrationApplication',)

from .bases import DiscordEntity, IconSlot
from .client_core import INTEGRATIONS
from .user import User, ZEROUSER
from .others import parse_time, DISCORD_EPOCH_START
from .role import PartialRole
from .http import URLS

from . import role

def PartialIntegration(integration_id, role=None):
    """
    Creates an integartion with the given id.
    
    If the integration already exists, returns that instead.
    
    Parameters
    ----------
    integration_id : `int`
        The unique identificator number of the integration.
    role : ``Role``, Optional
        The role of the integration.
    
    Returns
    -------
    integration : ``Integration``
    """
    try:
        integration = INTEGRATIONS[integration_id]
    except KeyError:
        integration = object.__new__(Integration)
        integration.id = integration_id
        integration.name = ''
        integration.type = ''
        integration.enabled = False
        integration.syncing = False
        integration.role = role
        integration.expire_behavior = 0
        integration.expire_grace_period = -1
        integration.user = ZEROUSER
        integration.account = IntegrationAccount.create_empty()
        integration.synced_at = DISCORD_EPOCH_START
        integration.subscriber_count = 0
        integration.application = None
        
    return integration

class Integration(DiscordEntity, immortal=True):
    """
    Represents a Discord Integration.
    
    id : `int`
        The unique identificator number of the integration.
    account : ``IntegrationAccount``, ``Client``, ``User``
        The integration's respective account. If the integration type is `'discord'`, then set as a discord user
        itself.
    application : `None` or ``Application``
        The application of the integration if applicable.
    enabled : `bool`
        Whether this integration is enabled.
    expire_behaviour : `int`
        The behavior of expiring subscription. `0` for kick or `1` for remove role.
    expire_grace_period : `int`
        The grace period in days for expiring subscribers. Can be `1`, `3`, `7`, `14` or `30`. If the integration is
        partial, then set as `-1`.
    name : `str`
        The name of the integration.
    role : `None` or ``Role``
        The role what the integration uses for subscribers.
    subscriber_count : `int`
        How many subscribers the integration has. Defaults to `0`.
    synced_at : `datetime`
        When the integration was last synced.
    syncing : `bool`
        Whether the integration syncing.
    type : `str`
        The type of the intgation (`'twitch'`, `'youtube'`, `'disocrd'`, ).
    user : ``Client`` or ``User``
        User for who the integration is. Defaults to `ZEROUSER`
    """
    __slots__ = ('account', 'application', 'enabled', 'expire_behavior', 'expire_grace_period', 'name', 'role',
        'subscriber_count', 'synced_at', 'syncing', 'type', 'user',)
    
    def __new__(cls, data):
        """
        Creates a new integration object with the given data. If the integration already exists, then updates and
        returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Integration data received from Discord.
        
        Returns
        -------
        integration : ``Intgraiton``
        """
        integration_id = int(data['id'])
        try:
            self = INTEGRATIONS[integration_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = integration_id
            
            update = True
        else:
            update = False
        
        self.name = data['name']
        self.type = integration_type = data['type']
        
        self.account = IntegrationAccount(data['account'], integration_type)
        
        self.enabled = data['enabled']
        self.syncing = data['syncing']
        self.role = PartialRole(int(data['role_id']))
        self.expire_behavior = data['expire_behavior']
        self.expire_grace_period = data['expire_grace_period']
        
        user_data = data.get('user')
        if user_data is None:
            user = ZEROUSER
        else:
            user = User(user_data)
        self.user = user
        
        self.synced_at = parse_time(data['synced_at'])
        self.subscriber_count = data['subscriber_count']
        
        application_data = data.get('application')
        if application_data is None:
            application = None
        else:
            application = IntegrationApplication(application_data)
        
        if update:
            self.application = application
        else:
            if (application is not None):
                self.application = application
        
        return self
    
    @property
    def partial(self):
        """
        Reuturns whether the integration is partial.
        
        Returns
        -------
        partial : `bool`
        """
        return (self.expire_grace_period == -1)
    
    def __str__(self):
        """Returns the integration's name."""
        return self.name
    
    def __repr__(self):
        """Returns the integration's representation."""
        return f'<{self.__class__.__name__} type={self.type}, id={self.id}, user={self.user.full_name!r}>'

class IntegrationAccount(object):
    """
    Account for who an ``Integration`` is for.
    
    Attributes
    ----------
    id : `str`
        The respective account's id.
    name : `str`
        The respective account's name
    """
    __slots__ = ('id', 'name', )
    def __new__(cls, data, integration_type):
        """
        Creates a new integration account instance from the given account data and integration type.
        
        If `integration_type` is `'discord'`, then returns a Discord user instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Integration account data.
        
        Returns
        -------
        self : ``IntegrationAccount``, ``User``, ``Client``
        """
        name = data['name']
        id_ = data['id']
        if integration_type == 'discord':
            self = User.precreate(id_, name=name, is_bot=True)
        else:
            self = object.__new__(cls)
            self.name = name
            self.id = id_
        
        return self
    
    def __repr__(self):
        """Returns the integration account's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, id={self.id!r}>'
    
    @classmethod
    def create_empty(cls):
        """
        Creates an empty integration account, with it's attributes set as empty strings.
        """
        self = object.__new__(cls)
        self.id = ''
        self.name = ''
        return self

class IntegrationApplication(DiscordEntity):
    """
    Represents a Discord ``Application`` received with Integration data.
    
    Attributes
    ----------
    bot : ``Client`` or ``User``
        The application's bot if applicable.
    description : `str`
        The description of the application. Defaults to empty string.
    icon_hash : `int`
        The application's icon's hash as `uint128`.
    icon_type : `IconType`
        The application's icon's type.
    id : `int`
        The application's id.
    name : `str`
        The name of the application. Defaults to empty string.
    summary : `str`
        if this application is a game sold on Discord, this field will be the summary field for the store page of its
        primary sku. Defautls to empty string.
    """
    __slots__ = ('bot', 'description', 'name', 'summary', )
    
    icon = IconSlot('icon', 'icon', URLS.application_icon_url, URLS.application_icon_url_as,)
    
    def __init__(self, data):
        """
        Creates a new integration application instance with the given application data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Application data included within integration payload.
        """
        self.id = int(data['id'])
        self.name = data['name']
        self.description = data['description']
        self.summary = data['summary']
        self._set_icon(data)
        
        bot_data = data.get('bot')
        if bot_data is None:
            bot = ZEROUSER
        else:
            bot = User(bot_data)
        
        self.bot = bot



# Scopes
role.PartialIntegration = PartialIntegration

del DiscordEntity
del role
del URLS
del IconSlot
