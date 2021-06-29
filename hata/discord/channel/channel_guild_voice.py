__all__ = ('ChannelStage', 'ChannelVoice', 'ChannelVoiceBase')

try:
    from _weakref import WeakSet
except ImportError:
    from weakref import WeakSet

from ...backend.utils import copy_docs
from ...backend.export import export, include

from ..core import CHANNELS
from ..permission import Permission
from ..permission.permission import PERMISSION_NONE, PERMISSION_TEXT_DENY, PERMISSION_STAGE_MODERATOR, \
    PERMISSION_VOICE_DENY_CONNECTION, PERMISSION_TEXT_AND_STAGE_DENY

from ..preconverters import preconvert_snowflake, preconvert_str, preconvert_int, preconvert_preinstanced_type

from .preinstanced import VideoQualityMode
from .channel_guild_base import ChannelGuildMainBase
from .channel_base import ChannelBase

VoiceRegion = include('VoiceRegion')

@export
class ChannelVoiceBase(ChannelGuildMainBase):
    """
    Base class for guild voice channels.
    
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
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    region : `None` or ``VoiceRegion``
        The voice region of the channel. If set as `None`, defaults to the voice channel's guild's.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `2`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `2`
        An order group what defined which guild channel type comes after the other one.
    """
    __slots__ = ('bitrate', 'region', 'user_limit') # Voice related.
    
    DEFAULT_TYPE = 2
    ORDER_GROUP = 2
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelVoiceBase, cls)._create_empty(channel_id, channel_type, partial_guild)
        
        self.bitrate = 0
        self.region = None
        self.user_limit = 0
        
        return self
    
    @property
    def voice_users(self):
        """
        Returns a list of the users, who are in the voice channel.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        users = []
        guild = self.guild
        if guild is None:
            return users
        
        for state in guild.voice_states.values():
            if state.channel is self:
                users.append(state.user)
        
        return users

    @property
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name


@export
class ChannelVoice(ChannelVoiceBase):
    """
    Represents a ``Guild`` voice channel.
    
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
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    region : `None` or ``VoiceRegion``
        The voice region of the channel. If set as `None`, defaults to the voice channel's guild's.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    video_quality_mode : ``VideoQualityMode``
        The video quality of the voice channel.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `2`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `(2,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `2`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `2`
        The channel's Discord side type.
    """
    __slots__ = ('video_quality_mode',) # Voice channel related
    
    INTERCHANGE = (2,)
    type = 2
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a voice channel from the channel data received from Discord. If the channel already exists and if it is
        partial, then updates it.
        
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
        else:
            if self.clients:
                return self
        
        # Guild base
        self._cache_perm = None
        self.name = data['name']
        
        self._init_parent_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        # Voice base
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
        
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        # Voice
        self.video_quality_mode = VideoQualityMode.get(data.get('video_quality_mode', 1))
        
        return self
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelVoice, cls)._create_empty(channel_id, channel_type, partial_guild)
        
        self.video_quality_mode = VideoQualityMode.auto
        
        return self
    
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.parent = None
        
        # safe delete
        if self is guild.afk_channel:
            guild.afk_channel = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self._cache_perm = None
        self._set_parent_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
        
        self.video_quality_mode = VideoQualityMode.get(data.get('video_quality_mode', 1))
    
    def _update(self, data):
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
        
        +-----------------------+-----------------------------------+
        | Keys                  | Values                            |
        +=======================+===================================+
        | bitrate               | `int`                             |
        +-----------------------+-----------------------------------+
        | parent                | ``ChannelCategory``               |
        +-----------------------+-----------------------------------+
        | name                  | `str`                             |
        +-----------------------+-----------------------------------+
        | overwrites            | `list` of ``PermissionOverwrite`` |
        +-----------------------+-----------------------------------+
        | position              | `int`                             |
        +-----------------------+-----------------------------------+
        | region                | `None` or ``VoiceRegion``         |
        +-----------------------+-----------------------------------+
        | user_limit            | `int`                             |
        +-----------------------+-----------------------------------+
        | video_quality_mode    | ``VideoQualityMode``              |
        +-----------------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        bitrate = data['bitrate']
        if self.bitrate != bitrate:
            old_attributes['bitrate'] = self.bitrate
            self.bitrate = bitrate
        
        user_limit = data['user_limit']
        if self.user_limit != user_limit:
            old_attributes['user_limit'] = self.user_limit
            self.user_limit = user_limit
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        
        if self.region is not region:
            old_attributes['region'] = self.region
            self.region = region
        
        self._update_parent_and_position(data, old_attributes)
        
        video_quality_mode = VideoQualityMode.get(data.get('video_quality_mode', 1))
        if self.video_quality_mode is not video_quality_mode:
            old_attributes['video_quality_mode'] = self.video_quality_mode
            self.video_quality_mode = video_quality_mode
        
        return old_attributes
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_TEXT_DENY
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        #voice channels don't have text permissions
        result &= PERMISSION_TEXT_AND_STAGE_DENY
        
        if not Permission.can_connect(result):
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
        return Permission(result)
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
        result = self._permissions_for_roles(roles)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # voice channels don't have text permissions
        result &= PERMISSION_TEXT_AND_STAGE_DENY
        
        if not Permission.can_connect(result):
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
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
        bitrate : `int`, Optional (Keyword only)
            The channel's ``.bitrate``.
        user_limit : `int`, Optional (Keyword only)
            The channel's ``.user_limit``.
        region : `None`, ``VoiceRegion`` or `str`, Optional (Keyword only)
            The channel's voice region.
        video_quality_mode : ``VideoQualityMode``, Optional (Keyword only)
            The video quality of the voice channel.
        
        Returns
        -------
        channel : ``ChannelVoice``
        
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
            
            for key, details in (
                    ('bitrate'   , (8000, 384000)),
                    ('user_limit', (    0,    99)),
                        ):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    value = preconvert_int(value, key, *details)
                    processable.append((key,value))
            
            for key, type_, nullable in (
                    ('region', VoiceRegion, True),
                    ('video_quality_mode', VideoQualityMode, False)
                        ):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    if nullable and (value is None):
                        continue
                    
                    value = preconvert_preinstanced_type(value, key, type_)
                    processable.append((key, value))
            
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



@export
class ChannelStage(ChannelVoiceBase):
    """
    Represents a Discord stage channel.
    
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
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    region : `None` or ``VoiceRegion``
        The voice region of the channel. If set as `None`, defaults to the voice channel's guild's.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    topic : `None` or `str`
        The channel's topic.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `13`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `(13,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `2`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `13`
        The channel's Discord side type.
    """
    __slots__ = ('topic',) # Stage channel related
    
    DEFAULT_TYPE = 13
    INTERCHANGE = (13,)
    type = 13
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a stage channel from the channel data received from Discord. If the channel already exists and if it is
        partial, then updates it.
        
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
        else:
            if self.clients:
                return self
        
        # Guild base
        self._cache_perm = None
        self.name = data['name']
        
        self._init_parent_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        # Voice base
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
        
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        self.topic = data.get('topic', None)
        
        return self
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelStage, cls)._create_empty(channel_id, channel_type, partial_guild)
        
        self.topic = None
        
        return self
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.parent = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self._cache_perm = None
        self._set_parent_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
        
        self.topic = None
    
    def _update(self, data):
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
        
        +-----------------------+-----------------------------------+
        | Keys                  | Values                            |
        +=======================+===================================+
        | bitrate               | `int`                             |
        +-----------------------+-----------------------------------+
        | parent                | ``ChannelCategory``  |
        +-----------------------+-----------------------------------+
        | name                  | `str`                             |
        +-----------------------+-----------------------------------+
        | overwrites            | `list` of ``PermissionOverwrite`` |
        +-----------------------+-----------------------------------+
        | position              | `int`                             |
        +-----------------------+-----------------------------------+
        | region                | `None` or ``VoiceRegion``         |
        +-----------------------+-----------------------------------+
        | user_limit            | `int`                             |
        +-----------------------+-----------------------------------+
        | topic                 | `None` or `int`                   |
        +-----------------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        bitrate = data['bitrate']
        if self.bitrate != bitrate:
            old_attributes['bitrate'] = self.bitrate
            self.bitrate = bitrate
        
        user_limit = data['user_limit']
        if self.user_limit != user_limit:
            old_attributes['user_limit'] = self.user_limit
            self.user_limit = user_limit
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        
        if self.region is not region:
            old_attributes['region'] = self.region
            self.region = region
        
        self._update_parent_and_position(data, old_attributes)
        
        topic = data.get('topic', None)
        if self.topic != topic:
            old_attributes['topic'] = self.topic
            self.topic = topic
        
        return old_attributes

    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_TEXT_DENY
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # voice channels don't have text permissions
        result &= PERMISSION_TEXT_DENY
        
        if not Permission.can_connect(result):
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
        return Permission(result)
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
        result = self._permissions_for_roles(roles)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # voice channels don't have text permissions
        result &= PERMISSION_TEXT_DENY
        
        if not Permission.can_connect(result):
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
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
        bitrate : `int`, Optional (Keyword only)
            The channel's ``.bitrate``.
        user_limit : `int`, Optional (Keyword only)
            The channel's ``.user_limit``.
        region : `None`, ``VoiceRegion`` or `str`, Optional (Keyword only)
            The channel's voice region.
        topic : `None` or `str`, Optional (Keyword only)
            The channel's topic.
        
        Returns
        -------
        channel : ``ChannelStage``
        
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
            
            for key, details in (
                    ('bitrate'   , (8000, 384000)),
                    ('user_limit', (    0,    99)),
                        ):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    value = preconvert_int(value, key, *details)
                    processable.append((key,value))
            
            try:
                region = kwargs.pop('region')
            except KeyError:
                pass
            else:
                if (region is not None):
                    region = preconvert_preinstanced_type(region, 'type_', VoiceRegion)
                    processable.append(('region', region))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
            
            try:
                topic = kwargs.pop('topic')
            except KeyError:
                pass
            else:
                if (topic is not None):
                    topic = preconvert_str(topic, 'topic', 0, 120)
                    if topic:
                        processable.append((topic, topic))
        
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
    
    @property
    def audience(self):
        """
        Returns the audience in the stage channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        users = []
        guild = self.guild
        if guild is None:
            return users
        
        for state in guild.voice_states.values():
            if (state.channel is self) and state.is_speaker:
                users.append(state.user)
        
        return users
    
    @property
    def speakers(self):
        """
        Returns the speakers in the stage channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        users = []
        guild = self.guild
        if guild is None:
            return users
        
        for state in guild.voice_states.values():
            if (state.channel is self) and (not state.is_speaker):
                users.append(state.user)
        
        return users
    
    @property
    def moderators(self):
        """
        Returns the moderators in the stage channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        users = []
        guild = self.guild
        if guild is None:
            return users
        
        for state in guild.voice_states.values():
            if (state.channel is self):
                user = state.user
                if self.permissions_for(user) >= PERMISSION_STAGE_MODERATOR:
                    users.append(user)
        
        return users
