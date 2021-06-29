__all__ = ('ChannelGuildUndefined', )

from ...backend.utils import copy_docs
from ...backend.export import export

from ..core import CHANNELS
from ..permission import Permission
from ..permission.permission import PERMISSION_NONE, PERMISSION_TEXT_AND_VOICE_DENY
from ..preconverters import preconvert_snowflake, preconvert_str, preconvert_int

from .channel_base import ChannelBase
from .channel_guild_base import ChannelGuildMainBase

@export
class ChannelGuildUndefined(ChannelGuildMainBase):
    """
    Represents an undefined  ``Guild`` channel. This class is a place-holder for future classes. Expectedly for channel
    type `7` and `8`.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermissionOverwrite`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    type : `int`
        The channel's type.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `7`
        The default type, what ``ChannelGuildUndefined`` represents.
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    IGNORED_NAMES : `frozenset` or `str`
        Attribute names, which will not be set automatically, because they are set by other modules.
    REPRESENTED_TYPES : `tuple` = (`7`, `8`,)
        The type values which ``ChannelGuildUndefined`` might represent.
    
    Notes
    -----
    This type supports dynamic attributes.
    """
    __slots__ = ('type', '__dict__', )
    
    DEFAULT_TYPE = 7
    IGNORED_NAMES = frozenset(('type', 'name', 'position', 'parent_id', 'permission_overwrites', ))
    INTERCHANGE = ()
    ORDER_GROUP = 0
    REPRESENTED_TYPES = (7, 8, )
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates an undefined guild channel from the channel data received from Discord. If the channel already exists
        and if it is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        assert (guild is not None), f'`guild` parameter cannot be `None` when calling `{cls.__name__}.__new__`.'
        
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
        
        self._cache_perm = None
        self.name = data['name']
        self.type = data['type']
        
        self._init_parent_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            setattr(self, key, data[key])
        
        return self
    
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        self = super(ChannelGuildUndefined, cls)._from_partial_data(data, channel_id, partial_guild)
        
        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            setattr(self, key, data[key])
        
        return self
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelGuildUndefined, cls)._create_empty(channel_id, channel_type, partial_guild)
        
        self.type = channel_type
        
        return self
    
    
    @property
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name
    
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self._cache_perm = None
        self._set_parent_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        
        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            setattr(self, key, data[key])
    
    def _update(self,data):
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
            All item in the returned dict is optional, and it might contain extra items.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------------------------------+
        | Keys          | Values                            |
        +===============+===================================+
        | parent        | ``ChannelCategory``               |
        +---------------+-----------------------------------+
        | name          | `str`                             |
        +---------------+-----------------------------------+
        | overwrites    | `list` of ``PermissionOverwrite`` |
        +---------------+-----------------------------------+
        | position      | `int`                             |
        +---------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        self._update_parent_and_position(data, old_attributes)

        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            old_value = getattr(self, key, ...)
            new_value = data[key]
            
            if old_value is ...:
                setattr(self, key, new_value)
            else:
                if old_value != new_value:
                    setattr(self, key, new_value)
                    old_attributes[key] = old_value
        
        return old_attributes
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        
        try:
            del guild.channels[self.id]
        except KeyError:
            pass
        
        self.parent = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self,user):
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_TEXT_AND_VOICE_DENY
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
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
        type : `int`, Optional (Keyword only)
            The channel's ``.type``.
        
        Returns
        -------
        channel : ``ChannelThread``
        
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
            
            try:
                type_ = kwargs.pop('type')
            except KeyError:
                pass
            else:
                type_ = preconvert_int(type_, 'type', 0, 255)
                processable.append(('type', type_))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.DEFAULT_TYPE, None)
            CHANNELS[channel_id] = self
            
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self


