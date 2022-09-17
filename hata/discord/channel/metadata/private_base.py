__all__ = ('ChannelMetadataPrivateBase',)

from scarletio import copy_docs

from ..fields.users import parse_users, put_users_into, validate_users

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
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('users',)
    
    @classmethod
    @copy_docs(ChannelMetadataBase.from_data)
    def from_data(cls, data):
        self = super(ChannelMetadataPrivateBase, cls).from_data(data)
        
        # users
        self.users = parse_users(data)
        
        return self
    
    
    @copy_docs(ChannelMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if self.users != other.users:
            return False
        
        return True
    
    
    @copy_docs(ChannelMetadataBase._get_users)
    def _get_users(self, channel_entity):
        return self.users
    
    
    @copy_docs(ChannelMetadataBase._iter_users)
    def _iter_users(self):
        yield from self.users
    
    
    @copy_docs(ChannelMetadataBase.name)
    def name(self):
        users = self.users
        if len(users) == 2:
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
    

    @copy_docs(ChannelMetadataBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        ChannelMetadataBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
        
        # users
        try:
            users = keyword_parameters.pop('users')
        except KeyError:
            pass
        else:
            self.users = validate_users(users)
    
    
    @copy_docs(ChannelMetadataBase.to_data)
    def to_data(self):
        data = ChannelMetadataBase.to_data(self)
        
        # users
        put_users_into(self.users, data, True)
        
        return data
