__all__ = ('ChannelMetadataPrivateBase',)

from scarletio import copy_docs

from ...user import User

from .base import ChannelMetadataBase


class ChannelMetadataPrivateBase(ChannelMetadataBase):
    """
    Channel metadata for private channels.
    
    Attributes
    ----------
    users : `list` of ``ClientUserBase``
        The users in the channel.
    
    Class Attributes
    ----------------
    type : `int` = `-1`
        The channel's type.
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('users',)
    
    @copy_docs(ChannelMetadataBase.__new__)
    def __new__(cls, data):
        self = ChannelMetadataBase.__new__(cls, data)
        
        users = []
        for user_data in data['recipients']:
            user = User.from_data(user_data)
            users.append(user)
        
        users.sort()
        self.users = users
        
        return self
    
    
    @copy_docs(ChannelMetadataBase._compare_attributes_to)
    def _compare_attributes_to(self, other):
        if self.users != other.users:
            return False
        
        return True
    
    
    @copy_docs(ChannelMetadataBase._get_users)
    def _get_users(self, channel_entity):
        return self.users
    
    
    @copy_docs(ChannelMetadataBase.name)
    def name(self):
        users = self.users
        if users:
            name = f'Direct Message {users[0].full_name} with {users[1].full_name}'
        else:
            name = f'Direct Message (partial)'
        return name
    
    
    @classmethod
    @copy_docs(ChannelMetadataBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataPrivateBase, cls)._create_empty()
        
        self.users = []
        
        return self
    
    
    @copy_docs(ChannelMetadataBase._to_data)
    def _to_data(self):
        data = ChannelMetadataBase.to_data(self)
        
        # users
        data['recipients'] = [user.to_data() for user in self.users]
        
        return self
