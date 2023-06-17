__all__ = ('ChannelMetadataPrivateGroup',)

from scarletio import copy_docs

from ...bases import ICON_TYPE_NONE, Slotted
from ...permission.permission import PERMISSION_GROUP, PERMISSION_GROUP_OWNER, PERMISSION_NONE

from .fields import (
    parse_application_id, parse_name, parse_owner_id, put_application_id_into, put_name_into, put_owner_id_into,
    validate_application_id, validate_name, validate_owner_id
)
from .base import CHANNEL_METADATA_ICON_SLOT
from .private_base import ChannelMetadataPrivateBase


class ChannelMetadataPrivateGroup(ChannelMetadataPrivateBase, metaclass = Slotted):
    """
    Channel metadata for private channels.
    
    Attributes
    ----------
    application_id : `int`
        The application's identifier the channel is managed by.
    icon_hash : `int`
        The channel's icon's hash in `uint128`.
    icon_type : ``iconType``
        The channel's icon's type.
    name : `str`
        The channel's display name. Can be empty string if the channel has no name.
    owner_id : `int`
        The group channel's owner's id.
    users : `list` of ``ClientUserBase``
        The users in the channel.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('application_id', 'name', 'owner_id')
    
    icon = CHANNEL_METADATA_ICON_SLOT
    
    
    def __new__(
        cls,
        *,
        application_id = ...,
        icon = ...,
        name = ...,
        owner_id = ...,
        users = ...,
    ):
        """
        Creates a new private group channel metadata from the given parameters.
        
        Parameters
        ----------
        application_id : `int`, ``Application``, Optional (Keyword only)
            The application's identifier the channel is managed by.
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The channel's icon.
        name : `str`, Optional (Keyword only)
            The channel's display name. Can be empty string if the channel has no name.
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The group channel's owner's id.
        users : `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The users in the channel.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # application_id
        if application_id is ...:
            application_id = 0
        else:
            application_id = validate_application_id(application_id)
        
        # icon
        if icon is ...:
            icon = None
        else:
            icon = cls.icon.validate_icon(icon, allow_data = True)
            
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # owner_id
        if owner_id is ...:
            owner_id = 0
        else:
            owner_id = validate_owner_id(owner_id)
    
        # Construct
        self = ChannelMetadataPrivateBase.__new__(
            cls,
            users = users,
        )
        self.application_id = application_id
        self.icon = icon
        self.name = name
        self.owner_id = owner_id
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataPrivateBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            application_id = keyword_parameters.pop('application_id', ...),
            icon = keyword_parameters.pop('icon', ...),
            name = keyword_parameters.pop('name', ...),
            owner_id = keyword_parameters.pop('owner_id', ...),
            users = keyword_parameters.pop('users', ...),
        )
    
    
    @copy_docs(ChannelMetadataPrivateBase.__hash__)
    def __hash__(self):
        hash_value = ChannelMetadataPrivateBase.__hash__(self)
        
        # application_id
        hash_value ^= self.application_id
        
        # icon
        hash_value ^= hash(self.icon)
        
        # name
        name = self.name
        if name:
            hash_value ^= hash(name)
        
        # owner_id
        hash_value ^= self.owner_id
        
        return hash_value
    
    
    @classmethod
    @copy_docs(ChannelMetadataPrivateBase.from_data)
    def from_data(cls, data):
        self = super(ChannelMetadataPrivateGroup, cls).from_data(data)
        
        # application_id
        self.application_id = parse_application_id(data)
        
        return self
    
    
    @copy_docs(ChannelMetadataPrivateBase._created)
    def _created(self, channel_entity, client, strong_cache):
        if strong_cache and (client is not None):
            client.group_channels[channel_entity.id] = channel_entity
    
        
    @copy_docs(ChannelMetadataPrivateBase._delete)
    def _delete(self, channel_entity, client):
        if (client is not None):
            try:
                del client.group_channels[channel_entity.id]
            except KeyError:
                pass
    
    
    @copy_docs(ChannelMetadataPrivateBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ChannelMetadataPrivateBase._is_equal_same_type(self, other):
            return False
        
        # application_id
        if self.application_id != other.application_id:
            return False
        
        # icon
        if self.icon_hash != other.icon_hash:
            return False
        
        if self.icon_type is not other.icon_type:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # owner_id
        if self.owner_id != other.owner_id:
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
        
        # application_id
        # Ignore internal
        
        # icon
        self._set_icon(data)
        
        # name
        self.name = parse_name(data)
        
        # owner_id
        self.owner_id = parse_owner_id(data)
    
    
    @copy_docs(ChannelMetadataPrivateBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataPrivateBase._difference_update_attributes(self, data)
        
        # application_id
        # Ignore internal
        
        # icon
        self._update_icon(data, old_attributes)
        
        # name
        name = parse_name(data)
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        # owner_id
        owner_id = parse_owner_id(data)
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
        
        self.application_id = 0
        self.name = ''
        self.owner_id = 0
        
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        
        return self
    
    
    @copy_docs(ChannelMetadataPrivateBase.copy)
    def copy(self):
        new = ChannelMetadataPrivateBase.copy(self)
        new.application_id = self.application_id
        new.name = self.name
        new.owner_id = self.owner_id
        new.icon_hash = self.icon_hash
        new.icon_type = self.icon_type
        return new
    
    
    def copy_with(
        self,
        *,
        application_id = ...,
        icon = ...,
        name = ...,
        owner_id = ...,
        users = ...,
    ):
        """
        Copies the private group channel metadata with the given fields.
        
        Parameters
        ----------
        application_id : `int`, ``Application``, Optional (Keyword only)
            The application's identifier the channel is managed by.
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The channel's icon.
        name : `str`, Optional (Keyword only)
            The channel's display name. Can be empty string if the channel has no name.
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The group channel's owner's id.
        users : `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The users in the channel.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # application_id
        if application_id is ...:
            application_id = self.application_id
        else:
            application_id = validate_application_id(application_id)
        
        # icon
        if icon is ...:
            icon = self.icon
        else:
            icon = type(self).icon.validate_icon(icon, allow_data = True)
            
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # owner_id
        if owner_id is ...:
            owner_id = self.owner_id
        else:
            owner_id = validate_owner_id(owner_id)
    
        # Construct
        new = ChannelMetadataPrivateBase.copy_with(
            self,
            users = users,
        )
        new.application_id = application_id
        new.icon = icon
        new.name = name
        new.owner_id = owner_id
        return new
    
    
    @copy_docs(ChannelMetadataPrivateBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            application_id = keyword_parameters.pop('application_id', ...),
            icon = keyword_parameters.pop('icon', ...),
            name = keyword_parameters.pop('name', ...),
            owner_id = keyword_parameters.pop('owner_id', ...),
            users = keyword_parameters.pop('users', ...),
        )
    
    
    @copy_docs(ChannelMetadataPrivateBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataPrivateBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        type(self).icon.put_into(self.icon, data, defaults, as_data = not include_internals)
        put_name_into(self.name, data, defaults)
        
        if include_internals:
            put_application_id_into(self.application_id, data, defaults)
            put_owner_id_into(self.owner_id, data, defaults)
        
        return data
