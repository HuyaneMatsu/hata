__all__ = ('ChannelText',)


from ...backend.utils import copy_docs
from ...backend.export import export

from ..core import CHANNELS
from ..permission import Permission
from ..permission.permission import PERMISSION_NONE, PERMISSION_TEXT_DENY, PERMISSION_VOICE_DENY
from ..preconverters import preconvert_snowflake, preconvert_str, preconvert_int, preconvert_bool, \
    preconvert_int_options

from .channel_base import ChannelBase
from .channel_guild_base import ChannelGuildMainBase
from .channel_text_base import ChannelTextBase
from .channel_thread import AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_OPTIONS


CHANNEL_TEXT_NAMES = {
     0: None,
     5: 'announcements',
}

@export
class ChannelText(ChannelGuildMainBase, ChannelTextBase):
    """
    Represents a ``Guild`` text channel or an announcements channel. So the type of the channel is interchangeable
    between them. The channel's Discord side channel type is 0 (text) or 5 (announcements).
    
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
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _turn_message_keep_limit_on_at : `float`
        The LOOP_TIME time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reached it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    default_auto_archive_after : `int`
        The default duration (in seconds) for newly created threads to automatically archive the themselves. Defaults
        to `3600`. Can be one of: `3600`, `86400`, `259200`, `604800`.
    nsfw : `bool`
        Whether the channel is marked as non safe for work.
    slowmode : `int`
        The amount of time in seconds what a user needs to wait between it's each message. Bots and user accounts with
        `manage_messages` or `manage_channel` permissions are unaffected.
    topic : `None` or `str`
        The channel's topic.
    type : `int`
        The channel's Discord side type. Can be any of `.INTERCHANGE`.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `0`
        The preferred channel type, if there is no channel type included.
    INTERCHANGE : `tuple` of `int` = `(0, 5,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    """
    __slots__ = ('default_auto_archive_after', 'nsfw', 'slowmode', 'topic', 'type',) # guild text channel related
    
    ORDER_GROUP = 0
    INTERCHANGE = (0, 5,)
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a guild text channel from the channel data received from Discord. If the channel already exists and if
        it is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
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
            self._messageable_init()
        else:
            if self.clients:
                return self
        
        self._cache_perm = None
        self.name = data['name']
        self.type = data['type']
        
        self._init_parent_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        self.topic = data.get('topic', None)
        self.nsfw = data.get('nsfw', False)
        
        slowmode = data.get('rate_limit_per_user', None)
        if slowmode is None:
            slowmode = 0
        self.slowmode = slowmode
        
        default_auto_archive_after = data.get('default_auto_archive_duration', None)
        if default_auto_archive_after is None:
            default_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        else:
            default_auto_archive_after *= 60
        self.default_auto_archive_after = default_auto_archive_after
        
        return self
    
    @copy_docs(ChannelBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        try:
            type_name = CHANNEL_TEXT_NAMES[self.type]
        except KeyError:
            type_name = repr(self.type)
        
        if (type_name is not None):
            repr_parts.append(' (')
            repr_parts.append(type_name)
            repr_parts.append(')')
            
        repr_parts.append(' id=')
        repr_parts.append(repr(self.id))
        repr_parts.append(', name=')
        repr_parts.append(repr(self.__str__()))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelText, cls)._create_empty(channel_id, channel_type, partial_guild)
        self._messageable_init()
        
        self.default_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        self.nsfw = False
        self.slowmode = 0
        self.topic = None
        self.type = channel_type
        
        return self
    
    
    @property
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name.lower()
    
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self._cache_perm = None
        self._set_parent_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        self.type = data['type']
        self.topic = data.get('topic', None)
        self.nsfw = data.get('nsfw', False)
        
        slowmode = data.get('rate_limit_per_user', None)
        if slowmode is None:
            slowmode = 0
        self.slowmode = slowmode
        
        default_auto_archive_after = data.get('default_auto_archive_duration', None)
        if default_auto_archive_after is None:
            default_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        else:
            default_auto_archive_after *= 60
        self.default_auto_archive_after = default_auto_archive_after
    
    def _update(self, data):
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
        +-------------------------------+-----------------------------------+
        | Keys                          | Values                            |
        +===============================+===================================+
        | default_auto_archive_after    | `int`                             |
        +-------------------------------+-----------------------------------+
        | parent                        | ``ChannelCategory``               |
        +-------------------------------+-----------------------------------+
        | name                          | `str`                             |
        +-------------------------------+-----------------------------------+
        | nsfw                          | `bool`                            |
        +-------------------------------+-----------------------------------+
        | overwrites                    | `list` of ``PermissionOverwrite`` |
        +-------------------------------+-----------------------------------+
        | position                      | `int`                             |
        +-------------------------------+-----------------------------------+
        | slowmode                      | `int`                             |
        +-------------------------------+-----------------------------------+
        | topic                         | `None` or `str`                   |
        +-------------------------------+-----------------------------------+
        | type                          | `int`                             |
        +-------------------------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}
        
        type_ = data['type']
        if self.type != type_:
            old_attributes['type'] = self.type
            self.type = type_
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        topic = data.get('topic', None)
        if self.topic != topic:
            old_attributes['topic'] = self.topic
            self.topic = topic
        
        nsfw = data.get('nsfw', False)
        if self.nsfw != nsfw:
            old_attributes['nsfw'] = self.nsfw
            self.nsfw = nsfw
        
        slowmode = data.get('rate_limit_per_user', None)
        if slowmode is None:
            slowmode = 0
        if self.slowmode != slowmode:
            old_attributes['slowmode'] = self.slowmode
            self.slowmode = slowmode
        
        default_auto_archive_after = data.get('default_auto_archive_duration', None)
        if default_auto_archive_after is None:
            default_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        else:
            default_auto_archive_after *= 60
        if self.default_auto_archive_after != default_auto_archive_after:
            old_attributes['default_auto_archive_after'] = self.default_auto_archive_after
            self.default_auto_archive_after = default_auto_archive_after
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        self._update_parent_and_position(data, old_attributes)
        
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
        
        if self is guild.system_channel:
            guild.system_channel = None
        if self is guild.widget_channel:
            guild.widget_channel = None
        if self is guild.rules_channel:
            guild.rules_channel = None
        if self is guild.public_updates_channel:
            guild.public_updates_channel = None
        
        self.parent = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_VOICE_DENY
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # text channels don't have voice permissions
        result &= PERMISSION_VOICE_DENY
        
        if self.type and (not Permission.can_manage_messages(result)):
            result = result&PERMISSION_TEXT_DENY
            return Permission(result)
        
        if not Permission.can_send_messages(result):
            result = result&PERMISSION_TEXT_DENY
        
        return Permission(result)
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
        result = self._permissions_for_roles(roles)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # text channels don't have voice permissions
        result &= PERMISSION_VOICE_DENY
        
        if self.type and (not Permission.can_manage_messages(result)):
            result = result&PERMISSION_TEXT_DENY
            return Permission(result)
        
        if not Permission.can_send_messages(result):
            result = result&PERMISSION_TEXT_DENY
        
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
        default_auto_archive_after : `int`, Optional (Keyword only)
            The channel's ``.default_auto_archive_after``.
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        topic : `None` or `str`, Optional (Keyword only)
            The channel's ``.topic``.
        slowmode : `int`, Optional (Keyword only)
            The channel's ``.slowmode``.
        type : `int`, Optional (Keyword only)
            The channel's ``.type``.
        nsfw : `int`, Optional (Keyword only)
            Whether the channel is marked as nsfw.
        
        Returns
        -------
        channel : ``ChannelText``
        
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
                value = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(value, 'name', 1, 100)
                processable.append(('name', name))
            
            try:
                topic = kwargs.pop('topic')
            except KeyError:
                pass
            else:
                if (topic is not None):
                    topic = preconvert_str(topic, 'topic', 0, 1024)
                    if topic:
                        processable.append(('topic', topic))
            
            try:
                slowmode = kwargs.pop('slowmode')
            except KeyError:
                pass
            else:
                slowmode = preconvert_int(slowmode, 'slowmode', 0, 21600)
                processable.append(('slowmode', slowmode))
            
            try:
                default_auto_archive_after = kwargs.pop('default_auto_archive_duration')
            except KeyError:
                pass
            else:
                default_auto_archive_after = preconvert_int_options(default_auto_archive_after,
                    'default_auto_archive_after', AUTO_ARCHIVE_OPTIONS)
                processable.append(('default_auto_archive_after', default_auto_archive_after))
            
            try:
                type_ = kwargs.pop('type')
            except KeyError:
                pass
            else:
                type_ = preconvert_int(type_, 'type', 0, 256)
                if (type_ not in cls.INTERCHANGE):
                    raise ValueError(f'`type` should be one of: {cls.INTERCHANGE!r}')
                
                processable.append(('type', type_))
            
            try:
                nsfw = kwargs.pop('nsfw')
            except KeyError:
                pass
            else:
                nsfw = preconvert_bool(nsfw, 'nsfw')
                processable.append(('nsfw', nsfw))
            
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

