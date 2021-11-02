__all__ = ('ChannelDirectory', )

from ...backend.utils import copy_docs
from ...backend.export import export, include

from ..core import CHANNELS
from ..permission import Permission
from ..permission.permission import PERMISSION_NONE, PERMISSION_THREAD_AND_VOICE_DENY, PERMISSION_MASK_VIEW_CHANNEL

from ..preconverters import preconvert_snowflake, preconvert_str

from .channel_base import ChannelBase
from .channel_text_base import ChannelTextBase
from .channel_guild_base import ChannelGuildMainBase

parse_permission_overwrites = include('parse_permission_overwrites')


@export
class ChannelDirectory(ChannelGuildMainBase, ChannelTextBase):
    """
    Represents a ``Guild`` directory channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _permission_cache : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent_id : `0`
        The channel's parent's identifier.
    guild_id : `int`
        The channel's guild's identifier.
    name : `str`
        The channel's name.
    permission_overwrites : `dict` of (`int`, ``PermissionOverwrite``) items
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    _message_history_collector :  `None` or ``MessageHistoryCollector``
        Collector for the channel's message history.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reached it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `14`
        The preferred channel type, if there is no channel type included.
    INTERCHANGE : `tuple` of `int` = `(14,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `14`
        The channel's Discord side type.
    """
    __slots__ = ()
    
    ORDER_GROUP = 0
    DEFAULT_TYPE = 14
    INTERCHANGE = (14, )
    type = 14
    
    
    def __new__(cls, data, client, guild_id):
        """
        Creates a directory channel from the channel data received from Discord. If the channel already exists and if
        it is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        client : `None` or ``Client``
            The client, who received the channel's data, if any.
        guild_id : `None` or ``Guild``
            The channel's guild's identifier.
        """
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
        else:
            if self.clients:
                return self
        
        self._permission_cache = None
        self.name = data['name']
        
        self._init_parent_and_position(data, guild_id)
        self.permission_overwrites = parse_permission_overwrites(data)
        
        return self
    
    # Ignore empty function, keep for reference
    """
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, guild_id):
        self = super(ChannelTextBase, cls)._create_empty(channel_id, channel_type, guild_id)
        return self
    """
    
    @property
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name.lower()
    
    
    @copy_docs(ChannelBase._update_attributes)
    def _update_attributes(self, data):
        self._permission_cache = None
        self._set_parent_and_position(data)
        self.permission_overwrites = parse_permission_overwrites(data)
        
        self.name = data['name']
    
        
    def _difference_update_attributes(self,data):
        """
        Updates the channel and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
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
        
        +---------------------------+---------------------------------------------------+
        | Keys                      | Values                                            |
        +===========================+===================================================+
        | parent_id                 | `int`                                             |
        +---------------------------+---------------------------------------------------+
        | name                      | `str`                                             |
        +---------------------------+---------------------------------------------------+
        | permission_overwrites     | `dict` of (`int`, ``PermissionOverwrite``) items  |
        +---------------------------+---------------------------------------------------+
        | position                  | `int`                                             |
        +---------------------------+---------------------------------------------------+
        """
        self._permission_cache = None
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        permission_overwrites = parse_permission_overwrites(data)
        if self.permission_overwrites != permission_overwrites:
            old_attributes['permission_overwrites'] = self.permission_overwrites
            self.permission_overwrites = permission_overwrites
        
        self._update_parent_and_position(data, old_attributes)
        
        return old_attributes
    
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        result = self._permissions_for(user)
        if not result&PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # directory channels do not have thread and voice related permissions
        result &= PERMISSION_THREAD_AND_VOICE_DENY
        
        return Permission(result)
    
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
        result = self._permissions_for_roles(roles)
        if not result&PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # directory channels do not have thread and voice related permissions
        result &= PERMISSION_THREAD_AND_VOICE_DENY
        return Permission(result)
    
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
        
        Returns
        -------
        channel : ``ChannelDirectory``
        
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
