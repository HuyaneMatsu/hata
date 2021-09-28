__all__ = ('ChannelPrivate', 'ChannelGroup', )

from ...backend.utils import copy_docs
from ...backend.export import export

from ..bases import IconSlot, ICON_TYPE_NONE
from ..core import CHANNELS
from ..permission.permission import PERMISSION_NONE, PERMISSION_PRIVATE, PERMISSION_PRIVATE_BOT, \
    PERMISSION_GROUP, PERMISSION_GROUP_OWNER
from ..user import User, ZEROUSER, create_partial_user_from_id
from ..preconverters import preconvert_snowflake, preconvert_str
from ..http import urls as module_urls

from .channel_base import ChannelBase
from .channel_text_base import ChannelTextBase

@export
class ChannelPrivate(ChannelBase, ChannelTextBase):
    """
    Represents a private (/ direct message) channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _message_history_collector :  `None` or ``MessageHistoryCollector``
        Collector for the channel's message history.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reached it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    users : `list` of ``ClientUserBase`` objects
        The channel's recipient.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `1`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `(1,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    type : `int` = `1`
        The channel's Discord side type.
    """
    __slots__ = ('users',) # private related
    
    DEFAULT_TYPE = 1
    INTERCHANGE = (1,)
    type = 1
    
    def __new__(cls, data, client, guild_id):
        """
        Creates a private channel from the channel data received from Discord. If the channel already exists and if it
        is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``
            The client, who received the channel's data, if any.
        guild_id : `int`
            The channel's guild's identifier.
        """
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
            self._messageable_init()
            self.users = users = []
        else:
            users = self.users
            if len(users) == 2:
                return self
            
            users.clear()
        
        for user_data in data['recipients']:
            user = User(user_data)
            users.append(user)
        
        if (client is not None):
            if client not in users:
                users.append(client)
            
            users.sort()
            
            user = users[0]
            if user is client:
                user = users[1]
                
            client.private_channels[user.id] = self
        
        return self
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, guild_id):
        self = super(ChannelPrivate, cls)._create_empty(channel_id, channel_type, guild_id)
        self._messageable_init()
        self.users = []
        
        return self
    
    
    @classmethod
    def _create_dataless(cls, channel_id):
        """
        Creates a private channel from a channel id. Might be called by events, when a message's channel is not found
        and it is a private channel.
        
        Parameters
        ----------
        channel_id : `int`
            The channel's respective id.
        
        Returns
        -------
        channel : ``ChannelPrivate``
            The created channel.
        """
        self = object.__new__(cls)
        self._messageable_init()
        self.id = channel_id
        self.users = []
        CHANNELS[channel_id] = self
        
        return self
    
    def _finish_dataless(self, client, user):
        """
        Finishes the initialization of the channel after a ``.create_dataless`` call.
        
        Parameters
        ----------
        client : ``Client``
            The client recipient of the channel.
        user : ``ClientUserBase``
            The other recipient of the channel.
        """
        users = self.users
        users.append(client)
        users.append(user)
        users.sort()
        
        client.private_channels[user.id] = self
    
    @copy_docs(ChannelBase._get_processed_name)
    def _get_processed_name(self):
        users = self.users
        if users:
            name = f'Direct Message {users[0].full_name} with {users[1].full_name}'
        else:
            name = f'Direct Message (partial)'
        return name
    
    
    def _delete(self, client):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        
        Parameters
        ----------
        client : ``Client``
            The client, who's private channel was deleted.
        """
        users = self.users
        if client is users[0]:
            user = users[1]
        else:
            user = users[0]
        
        del client.private_channels[user.id]
    
    
    name = property(_get_processed_name)
    copy_docs(ChannelBase.name)(name)
    
    display_name = property(_get_processed_name)
    copy_docs(ChannelBase.display_name)(display_name)
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        if user in self.users:
            if user.is_bot:
                return PERMISSION_PRIVATE_BOT
            else:
                return PERMISSION_PRIVATE
            
        return PERMISSION_NONE
    
    
    cached_permissions_for = permissions_for
    
    
    @classmethod
    def precreate(cls, channel_id, **kwargs):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precrated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int` or `str`
            The channel's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the channel.
        
        Returns
        -------
        channel : ``ChannelPrivate``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        channel_id = preconvert_snowflake(channel_id, 'channel_id')
        
        if kwargs:
            raise ValueError(f'Unused or unsettable attributes: {kwargs}')
        
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.type, 0)
            CHANNELS[channel_id] = self
        
        return self



@export
class ChannelGroup(ChannelBase, ChannelTextBase):
    """
    Represents a group channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _message_history_collector :  `None` or ``MessageHistoryCollector``
        Collector for the channel's message history.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reached it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    users : `list` of ``ClientUserBase`` objects
        The channel's recipient.
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
    DEFAULT_TYPE : `int` = `3`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `(3,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    type : `int` = `3`
        The channel's Discord side type.
    """
    __slots__ = ('users', # private channel related
        'name', 'owner_id',) # group channel related
    
    icon = IconSlot('icon', 'icon', module_urls.channel_group_icon_url, module_urls.channel_group_icon_url_as)
    
    DEFAULT_TYPE = 3
    INTERCHANGE = (3,)
    type = 3
    
    def __new__(cls, data, client, guild_id):
        """
        Creates a channel from the channel data received from Discord. If the channel already exists and if it is
        partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``
            The client, who received the channel's data, if any.
        guild_id : `int`
            The channel's guild's identifier.
        """
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
            self._messageable_init()
            self.users = users = []
        else:
            users = self.users
            if len(users) == len(data['recipients']):
                return self
            
            users.clear()
        
        name = data.get('name', None)
        self.name = '' if name is None else name
        self._set_icon(data)
        self.owner_id = int(data['owner_id'])
        
        for user_data in data['recipients']:
            user = User(user_data)
            users.append(user)
        
        users.sort()
        
        if (client is not None):
            client.group_channels[channel_id] = self
        
        return self
    
    
    @property
    def owner(self):
        """
        Returns the group channel's owner.
        
        Returns
        -------
        owner : ``ClientUserBase``
            Defaults to `ZEROUSER`.
        """
        owner_id = self.owner_id
        if owner_id:
            owner = create_partial_user_from_id(owner_id)
        else:
            owner = ZEROUSER
        return owner
    
    
    @classmethod
    @copy_docs(ChannelBase._from_partial_data)
    def _from_partial_data(cls, data, channel_id, guild_id):
        self = super(ChannelGroup, cls)._from_partial_data(data, channel_id, guild_id)
        
        name = data.get('name', None)
        if (name is not None):
            self.name = name
        
        return self
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, guild_id):
        self = super(ChannelGroup, cls)._create_empty(channel_id, channel_type, guild_id)
        self._messageable_init()
        
        self.users = []
        
        self.name = None
        self.owner_id = 0
        
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        
        return self
    
    
    def _delete(self, client):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        
        Parameters
        ----------
        client : ``Client``
            The client, who's private channel was deleted.
        """
        del client.group_channels[self.id]
    
    
    @copy_docs(ChannelBase._update_attributes)
    def _update_attributes(self, data):
        name = data.get('name', None)
        self.name = '' if name is None else name
        
        self._set_icon(data)
        
        self.owner_id = int(data['owner_id'])
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the channel and returns it's overwritten old attributes as a `dict` with a `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
            
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+---------------------------------------+
        | Keys          | Values                                |
        +===============+=======================================+
        | icon          | ``Icon``                              |
        +---------------+---------------------------------------+
        | name          | `str`                                 |
        +---------------+---------------------------------------+
        | owner_id      | `int`                                 |
        +---------------+---------------------------------------+
        """
        old_attributes = {}
        
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
    
    @copy_docs(ChannelBase._get_processed_name)
    def _get_processed_name(self):
        name = self.name
        if name:
            return name
        
        users = self.users
        if users:
            return ', '.join([user.name for user in users])
        
        return 'Unnamed'
    
    display_name = property(_get_processed_name)
    copy_docs(ChannelBase.display_name)(display_name)
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        if self.owner_id == user.id:
            return PERMISSION_GROUP_OWNER
        elif user in self.users:
            return PERMISSION_GROUP
        else:
            return PERMISSION_NONE
    
    cached_permissions_for = permissions_for
    
    
    @classmethod
    def precreate(cls, channel_id, **kwargs):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precrated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int` or `str`
            The channel's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the channel.
        
        Other Parameters
        ----------------
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        icon : `int`, Optional (Keyword only)
            The channel's ``.icon``.
        owner_id : `int`, Optional (Keyword only)
            The channel's owner's id.
        
        Returns
        -------
        channel : ``ChannelGroup``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        channel_id = preconvert_snowflake(channel_id, 'channel_id')
        
        if kwargs:
            processable = []
            
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 100)
                processable.append(('name', name))
            
            cls.icon.preconvert(kwargs, processable)
            
            try:
                owner_id = kwargs.pop('owner_id')
            except KeyError:
                pass
            else:
                owner_id = preconvert_snowflake(owner_id, 'owner_id')
                processable.append(('owner_id', owner_id))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.type, 0)
            CHANNELS[channel_id] = self
            
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
