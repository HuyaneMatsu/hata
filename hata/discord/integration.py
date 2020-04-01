# -*- coding: utf-8 -*-
__all__ = ('Integration', )

from .client_core import INTEGRATIONS, ROLES
from .user import User
from .others import parse_time, id_to_time

class Integration(object):
    __slots__=('__weakref__', 'account_id', 'account_name', 'enabled',
        'expire_behavior', 'expire_grace_period', 'id', 'name', 'role',
        'synced_at', 'syncing', 'type', 'user',)
    
    def __new__(cls,data):
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
        integration.role=ROLES.get(int(data['role_id']),None)
        integration.expire_behavior=data['expire_behavior']
        integration.expire_grace_period=data['expire_grace_period']
        integration.user=User(data['user'])
        integration.account_id=data['account']['id']
        integration.account_name=data['account']['name']
        integration.synced_at=parse_time(data['synced_at'])
        
        return integration
    
    def __hash__(self):
        return self.id

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'<{self.__class__.__name__} type={self.type} id={self.id} user={self.user.full_name}>'

    @property
    def created_at(self):
        return id_to_time(self.id)
