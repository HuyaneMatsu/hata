__all__ = ('ChannelMetadataPrivate',)

from scarletio import copy_docs

from ...permission.permission import PERMISSION_NONE, PERMISSION_PRIVATE, PERMISSION_PRIVATE_BOT

from .private_base import ChannelMetadataPrivateBase


class ChannelMetadataPrivate(ChannelMetadataPrivateBase):
    """
    Channel metadata for private channels.
    
    Attributes
    ----------
    users : `list` of ``ClientUserBase``
        The users in the channel.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ()
    
    @copy_docs(ChannelMetadataPrivateBase._created)
    def _created(self, channel_entity, client, strong_cache):
        if (client is not None):
            users = self.users
            if client not in users:
                users.append(client)
                users.sort()
            
            if strong_cache and len(users) >= 2:
                user = users[0]
                if client is user:
                    user = users[1]
                
                client.private_channels[user.id] = channel_entity
    
    
    @copy_docs(ChannelMetadataPrivateBase._delete)
    def _delete(self, channel_entity, client):
        if (client is not None):
            users = self.users
            if len(users) >= 2:
                
                user = users[0]
                if client is user:
                    user = users[1]
                
                del client.private_channels[user.id]
    
    
    @property
    @copy_docs(ChannelMetadataPrivateBase.name)
    def name(self):
        users = self.users
        if len(users) >= 2:
            name = f'Direct Message {users[0].full_name} with {users[1].full_name}'
        else:
            name = f'Direct Message (partial)'
        return name
    
    
    @copy_docs(ChannelMetadataPrivateBase._get_permissions_for)
    def _get_permissions_for(self, channel_entity, user):
        if user in self.users:
            if user.bot:
                return PERMISSION_PRIVATE_BOT
            else:
                return PERMISSION_PRIVATE
            
        return PERMISSION_NONE
