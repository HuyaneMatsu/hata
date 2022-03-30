__all__ = ('ChannelMetadataPrivateGroup',)


from scarletio import copy_docs

from ...bases import ICON_TYPE_NONE, IconSlot
from ...http import urls as module_urls
from ...permission.permission import PERMISSION_GROUP, PERMISSION_GROUP_OWNER, PERMISSION_NONE
from ...preconverters import preconvert_snowflake, preconvert_str

from .. import channel_types as CHANNEL_TYPES

from .private_base import ChannelMetadataPrivateBase


class ChannelMetadataPrivateGroup(ChannelMetadataPrivateBase):
    """
    Channel metadata for private channels.
    
    Attributes
    ----------
    users : `list` of ``ClientUserBase``
        The users in the channel.
    icon_hash : `int`
        The channel's icon's hash in `uint128`.
    icon_type : ``iconType``
        The channel's icon's type.
    name : `str`
        The channel's display name. Can be empty string if the channel has no name.
    owner_id : `int`
        The group channel's owner's id.
    
    Class Attributes
    ----------------
    type : `int` = `CHANNEL_TYPES.private_group`
        The channel's type.
    """
    __slots__ = ('name', 'owner_id')
    
    icon = IconSlot('icon', 'icon', module_urls.channel_group_icon_url, module_urls.channel_group_icon_url_as)
    
    type = CHANNEL_TYPES.private_group
    
    
    @copy_docs(ChannelMetadataPrivateBase._created)
    def _created(self, channel_entity, client):
        if (client is not None):
            client.group_channels[channel_entity.id] = channel_entity
    
        
    @copy_docs(ChannelMetadataPrivateBase._delete)
    def _delete(self, channel_entity, client):
        if (client is not None):
            try:
                del client.group_channels[channel_entity.id]
            except KeyError:
                pass
    
    
    @copy_docs(ChannelMetadataPrivateBase._compare_attributes_to)
    def _compare_attributes_to(self, other):
        if not ChannelMetadataPrivateBase._compare_attributes_to(self, other):
            return False
        
        if self.name != other.name:
            return False
        
        if self.owner_id != other.owner_id:
            return False
        
        if self.icon_hash != other.icon_hash:
            return False
        
        if self.icon_type is not other.icon_type:
            return False
        
        return True
    
    
    @copy_docs(ChannelMetadataPrivateBase._get_processed_name)
    def _get_processed_name(self):
        name = self.name
        if name:
            return name
        
        users = self.users
        if users:
            return ', '.join([user.name for user in users])
        
        return 'Unnamed'
    
    
    @copy_docs(ChannelMetadataPrivateBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataPrivateBase._update_attributes(self, data)
        
        name = data.get('name', None)
        if name is None:
            name = ''
        self.name = name
        
        self.owner_id = int(data['owner_id'])
        
        self._set_icon(data)
    
    
    @copy_docs(ChannelMetadataPrivateBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataPrivateBase._difference_update_attributes(self, data)
        
        name = data.get('name', None)
        if name is None:
            name = ''
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        self._update_icon(data, old_attributes)
        
        owner_id = int(data['owner_id'])
        if self.owner_id != owner_id:
            old_attributes['owner_id'] = self.owner_id
            self.owner_id = owner_id
        
        return old_attributes

    
    @copy_docs(ChannelMetadataPrivateBase._get_permissions_for)
    def _get_permissions_for(self, channel_entity, user):
        if self.owner_id == user.id:
            return PERMISSION_GROUP_OWNER
        elif user in self.users:
            return PERMISSION_GROUP
        else:
            return PERMISSION_NONE
    
    
    @classmethod
    @copy_docs(ChannelMetadataPrivateBase._from_partial_data)
    def _from_partial_data(cls, data):
        self = super(ChannelMetadataPrivateGroup, cls)._from_partial_data(data)
        
        if (data is not None):
            name = data.get('name', None)
            if (name is not None):
                self.name = name
        
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataPrivateBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataPrivateGroup, cls)._create_empty()
        
        self.name = None
        self.owner_id = 0
        
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataPrivateBase._precreate)
    def _precreate(cls, keyword_parameters):
        self = super(ChannelMetadataPrivateGroup, cls)._precreate(keyword_parameters)
        
        try:
            name = keyword_parameters.pop('name')
        except KeyError:
            pass
        else:
            name = preconvert_str(name, 'name', 2, 100)
            self.name = name
        
        
        processable = []
        cls.icon.preconvert(keyword_parameters, processable)
        if processable:
            for item in processable:
                setattr(self, *item)
        processable = None
        
        
        try:
            owner_id = keyword_parameters.pop('owner_id')
        except KeyError:
            pass
        else:
            owner_id = preconvert_snowflake(owner_id, 'owner_id')
            self.owner_id = owner_id
        
        return self
    
    
    @copy_docs(ChannelMetadataPrivateBase._to_data)
    def _to_data(self):
        data = ChannelMetadataPrivateBase.to_data(self)
        
        # name
        name = self.name
        if not name:
            name = None
        data['name'] = name
        
        # owner_id
        data['owner_id'] = str(self.owner_id)
        
        # icon
        data['icon'] = self.icon.as_base16_hash
        
        return self
