# -*- coding: utf-8 -*-
__all__ = ('Integration', )

from .bases import DiscordEntity
from .client_core import INTEGRATIONS
from .user import User
from .others import parse_time
from .role import PartialRole

class Integration(DiscordEntity, immortal=True):
    """
    Represents a Discord Integration.
    
    id : `int`
        The unique identificator numbr of the integration.
    account_id : `str`
        The integration's respective account's identificator.
    account_name : `str`
        The integration's respective account's name.
    enabled : `bool`
        Whether this integration is enabled.
    expire_behaviour : `int`
        The behavior of expiring subscription. `0` for kick or `1` for remove role.
    expire_grace_period : `int`
        The grace period in days for expiring subscribers. Can be `1`, `3`, `7`, `14` or `30`.
    name : `str`
        The name of the integration.
    role : `None` or ``Role``
        The role what the integration uses for subscribers.
    synced_at : `datetime`
        When the integration was last synced.
    syncing : `bool`
        Is the integration syncing.
    type : `str`
        The type of the intgation (`'twitch'`, `'youtube'`, etc).
    user : ``Client`` or ``User``
        User for who the integration is.
    """
    __slots__ = ('account_id', 'account_name', 'enabled', 'expire_behavior', 'expire_grace_period', 'name', 'role',
        'synced_at', 'syncing', 'type', 'user',)
    
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
        integration_id=int(data['id'])
        try:
            integration=INTEGRATIONS[integration_id]
        except KeyError:
            integration=object.__new__(cls)
            integration.id=integration_id
            
        integration.name=data['name']
        integration.type=data['type']
        integration.enabled=data['enabled']
        integration.syncing=data['syncing']
        integration.role=PartialRole(int(data['role_id']))
        integration.expire_behavior=data['expire_behavior']
        integration.expire_grace_period=data['expire_grace_period']
        integration.user=User(data['user'])
        integration.account_id=data['account']['id']
        integration.account_name=data['account']['name']
        integration.synced_at=parse_time(data['synced_at'])
        
        return integration
    
    def __str__(self):
        """Returns the integration's name."""
        return self.name
    
    def __repr__(self):
        """Returns the integration's representation."""
        return f'<{self.__class__.__name__} type={self.type}, id={self.id}, user={self.user.full_name!r}>'

del DiscordEntity
