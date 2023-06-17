__all__ = ('VoiceState', )

import warnings

from scarletio import RichAttributeErrorBaseType, include

from ...core import GUILDS

from ..user import create_partial_user_from_id

from .fields import (
    parse_channel_id, parse_deaf, parse_mute, parse_requested_to_speak_at, parse_self_deaf, parse_self_mute,
    parse_self_stream, parse_self_video, parse_session_id, parse_speaker, parse_user_id, put_channel_id_into,
    put_deaf_into, put_mute_into, put_requested_to_speak_at_into, put_self_deaf_into, put_self_mute_into,
    put_self_stream_into, put_self_video_into, put_session_id_into, put_speaker_into, put_user_id_into,
    validate_channel_id, validate_deaf, validate_guild_id, validate_mute, validate_requested_to_speak_at,
    validate_self_deaf, validate_self_mute, validate_self_stream, validate_self_video, validate_session_id,
    validate_speaker, validate_user_id
)


ChannelType = include('ChannelType')
create_partial_channel_from_id = include('create_partial_channel_from_id')
create_partial_role_from_id = include('create_partial_role_from_id')


class VoiceState(RichAttributeErrorBaseType):
    """
    Represents a user at a ``Channel``.
    
    Attributes
    ----------
    _cache_user : ``ClientUserBase``
        The voice state's respective user.
    channel_id : `int`
        The channel's identifier to where the user is connected to.
    deaf : `bool`
        Whether the user is deafen.
    guild_id : `int`
        The guild's identifier where the user is connected to.
    mute : `bool`
        Whether the user is muted.
    requested_to_speak_at : `None`, `datetime`
        When the user requested to speak.
        
        Only applicable in stage channels.
    
    self_deaf : `bool`
        Whether the user muted everyone else.
    self_mute : `bool`
        Whether the user muted itself.
    self_stream : `bool`
        Whether the user screen shares with the go live option.
    self_video : `bool`
        Whether the user sends video from a camera source.
    session_id : `str``
        The user's voice session id.
    speaker : `bool`
        Whether the user is suppressed inside of the voice channel.
        
        At voice channels it is always `False`, but in stage channels it can vary.
    
    user_id : `int`
        The voice state's respective user's identifier.
    """
    __slots__ = (
        '_cache_user', 'channel_id', 'deaf', 'guild_id', 'mute', 'requested_to_speak_at', 'self_deaf', 'self_mute',
        'self_stream', 'self_video', 'session_id', 'speaker', 'user_id'
    )
    
    
    def __new__(
        cls,
        *,
        channel_id = ...,
        deaf = ...,
        guild_id = ...,
        speaker = ...,
        mute = ...,
        requested_to_speak_at = ...,
        self_deaf = ...,
        self_mute = ...,
        self_stream = ...,
        self_video = ...,
        session_id = ...,
        user_id = ...,
    ):
        """
        Creates a new voice state with the given fields.
        
        Parameters
        ----------
        channel_id : `int`, Optional (Keyword only)
            The channel's identifier to where the user is connected to.
        deaf : `bool`, Optional (Keyword only)
            Whether the user is deafen.
        guild_id : `int`, Optional (Keyword only)
            The guild's identifier where the user is connected to.
        mute : `bool`, Optional (Keyword only)
            Whether the user is muted.
        requested_to_speak_at : `None`, `datetime`, Optional (Keyword only)
            When the user requested to speak.
        self_deaf : `bool`, Optional (Keyword only)
            Whether the user muted everyone else.
        self_mute : `bool`, Optional (Keyword only)
            Whether the user muted itself.
        self_stream : `bool`, Optional (Keyword only)
            Whether the user screen shares with the go live option.
        self_video : `bool`, Optional (Keyword only)
            Whether the user sends video from a camera source.
        session_id : `str``, Optional (Keyword only)
            The user's voice session id.
        speaker : `bool`, Optional (Keyword only)
            Whether the user is suppressed inside of the voice channel.
        user_id : `int`, Optional (Keyword only)
            The voice state's respective user's identifier.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = 0
        else:
            channel_id = validate_channel_id(channel_id)
        
        # deaf
        if deaf is ...:
            deaf = False
        else:
            deaf = validate_deaf(deaf)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # mute
        if mute is ...:
            mute = False
        else:
            mute = validate_mute(mute)
        
        # requested_to_speak_at
        if requested_to_speak_at is ...:
            requested_to_speak_at = None
        else:
            requested_to_speak_at = validate_requested_to_speak_at(requested_to_speak_at)
        
        # self_deaf
        if self_deaf is ...:
            self_deaf = False
        else:
            self_deaf = validate_self_deaf(self_deaf)
        
        # self_mute
        if self_mute is ...:
            self_mute = False
        else:
            self_mute = validate_self_mute(self_mute)
        
        # self_stream
        if self_stream is ...:
            self_stream = False
        else:
            self_stream = validate_self_stream(self_stream)
        
        # self_video
        if self_video is ...:
            self_video = False
        else:
            self_video = validate_self_video(self_video)
        
        # session_id
        if session_id is ...:
            session_id = ''
        else:
            session_id = validate_session_id(session_id)
        
        # speaker
        if speaker is ...:
            speaker = False
        else:
            speaker = validate_speaker(speaker)
        
        # user_id
        if user_id is ...:
            user_id = 0
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        self = object.__new__(cls)
        self._cache_user = None
        self.channel_id = channel_id
        self.deaf = deaf
        self.guild_id = guild_id
        self.mute = mute
        self.requested_to_speak_at = requested_to_speak_at
        self.self_deaf = self_deaf
        self.self_mute = self_mute
        self.self_stream = self_stream
        self.self_video = self_video
        self.session_id = session_id
        self.speaker = speaker
        self.user_id = user_id
        return self
    
    
    @classmethod
    def from_data(cls, data, guild_id, *, strong_cache = True):
        """
        Creates a voice state object from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Voice state data.
        guild_id : `int`
            The voice state's guild's identifier.
        strong_cache : `bool` = `True`, Optional (Keyword only)
            Whether the instance should be put into its strong cache.
        
        Returns
        -------
        new : `None`, `instance<cls>`
        """
        channel_id = parse_channel_id(data)
        if not channel_id:
            return
        
        user_id = parse_user_id(data)
        
        if strong_cache:
            guild = GUILDS.get(guild_id, None)
            if (guild is not None):
                try:
                    return guild.voice_states[user_id]
                except KeyError:
                    pass
        
        self = object.__new__(cls)
        self._cache_user = None
        self.channel_id = channel_id
        self.deaf = parse_deaf(data)
        self.guild_id = guild_id
        self.speaker = parse_speaker(data)
        self.mute = parse_mute(data)
        self.requested_to_speak_at = parse_requested_to_speak_at(data)
        self.self_deaf = parse_self_deaf(data)
        self.self_mute = parse_self_mute(data)
        self.self_stream = parse_self_stream(data)
        self.self_video = parse_self_video(data)
        self.session_id = parse_session_id(data)
        self.user_id = user_id
        
        if strong_cache:
            if (guild is not None):
                guild.voice_states[user_id] = self
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the voice state to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with the default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_channel_id_into(self.channel_id, data, defaults)
        put_deaf_into(self.deaf, data, defaults)
        put_mute_into(self.mute, data, defaults)
        put_requested_to_speak_at_into(self.requested_to_speak_at, data, defaults)
        put_self_deaf_into(self.self_deaf, data, defaults)
        put_self_mute_into(self.self_mute, data, defaults)
        put_self_stream_into(self.self_stream, data, defaults)
        put_self_video_into(self.self_video, data, defaults)
        put_session_id_into(self.session_id, data, defaults)
        put_speaker_into(self.speaker, data, defaults)
        put_user_id_into(self.user_id, data, defaults)
        return data
    
    
    def _update_attributes(self, data):
        """
        Updates the voice state with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Voice state data.
        """
        self.deaf = parse_deaf(data)
        self.mute = parse_mute(data)
        self.requested_to_speak_at = parse_requested_to_speak_at(data)
        self.self_deaf = parse_self_deaf(data)
        self.self_mute = parse_self_mute(data)
        self.self_stream = parse_self_stream(data)
        self.self_video = parse_self_video(data)
        self.speaker = parse_speaker(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the voice state and returns it's overwritten attributes as a `dict` with a `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Voice state data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            All item in the returned dictionary is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | deaf                  | `str`                 |
        +-----------------------+-----------------------+
        | mute                  | `bool`                |
        +-----------------------+-----------------------+
        | requested_to_speak_at | `None`, `datetime`    |
        +-----------------------+-----------------------+
        | self_deaf             | `bool`                |
        +-----------------------+-----------------------+
        | self_mute             | `bool`                |
        +-----------------------+-----------------------+
        | self_stream           | `bool`                |
        +-----------------------+-----------------------+
        | self_video            | `bool`                |
        +-----------------------+-----------------------+
        | speaker               | `bool`                |
        +-----------------------+-----------------------+
        """
        old_attributes = {}
        
        deaf = parse_deaf(data)
        if self.deaf != deaf:
            old_attributes['deaf'] = self.deaf
            self.deaf = deaf
        
        mute = parse_mute(data)
        if self.mute != mute:
            old_attributes['mute'] = self.mute
            self.mute = mute
        
        requested_to_speak_at = parse_requested_to_speak_at(data)
        if self.requested_to_speak_at != requested_to_speak_at:
            old_attributes['requested_to_speak_at'] = self.requested_to_speak_at
            self.requested_to_speak_at = requested_to_speak_at
        
        self_deaf = parse_self_deaf(data)
        if self.self_deaf != self_deaf:
            old_attributes['self_deaf'] = self.self_deaf
            self.self_deaf = self_deaf
        
        self_video = parse_self_video(data)
        if self.self_video != self_video:
            old_attributes['self_video'] = self.self_video
            self.self_video = self_video
        
        self_stream = parse_self_stream(data)
        if self.self_stream != self_stream:
            old_attributes['self_stream'] = self.self_stream
            self.self_stream = self_stream
        
        self_mute = parse_self_mute(data)
        if self.self_mute != self_mute:
            old_attributes['self_mute'] = self.self_mute
            self.self_mute = self_mute
        
        speaker = parse_speaker(data)
        if self.speaker != speaker:
            old_attributes['speaker'] = self.speaker
            self.speaker = speaker
        
        return old_attributes
    
    
    def _update_channel(self, data):
        """
        Updates the voice state's channel.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Voice state data.
        
        Returns
        -------
        old_channel_id : `int`
            The voice state's old channel's identifier.
        new_channel_id : `int`
            The voice state's new channel's identifier.
        """
        new_channel_id = parse_channel_id(data)
        if not new_channel_id:
            try:
                guild = GUILDS[self.guild_id]
            except KeyError:
                pass
            else:
                try:
                    del guild.voice_states[self.user_id]
                except KeyError:
                    pass
        
        old_channel_id = self.channel_id
        self.channel_id = new_channel_id
        
        return old_channel_id, new_channel_id
    
    
    def __repr__(self):
        """Returns the voice state's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append(', guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', channel_id = ')
        repr_parts.append(repr(self.channel_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two voice states are equal"""
        # Shortcut
        if self is other:
            return True
        
        if type(self) is not type(other):
            return NotImplemented
        
        # channel_id
        if self.channel_id != other.channel_id:
            return False
        
        # deaf
        if self.deaf != other.deaf:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # mute
        if self.mute != other.mute:
            return False
        
        # requested_to_speak_at
        if self.requested_to_speak_at != other.requested_to_speak_at:
            return False
        
        # self_deaf
        if self.self_deaf != other.self_deaf:
            return False
        
        # self_mute
        if self.self_mute != other.self_mute:
            return False
        
        # self_stream
        if self.self_stream != other.self_stream:
            return False
        
        # self_video
        if self.self_video != other.self_video:
            return False
        
        # session_id
        if self.session_id != other.session_id:
            return False
        
        # speaker
        if self.speaker != other.speaker:
            return False
        
        # user_id
        if self.user_id != other.user_id:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the voice state's hash value."""
        hash_value = 0
        
        # channel_id
        hash_value ^= self.channel_id
        
        # deaf
        hash_value ^= self.deaf << 0
        
        # guild_id
        hash_value ^= self.guild_id
        # mute
        hash_value ^= self.mute << 2
        
        # requested_to_speak_at
        requested_to_speak_at = self.requested_to_speak_at
        if (requested_to_speak_at is not None):
            hash_value ^= hash(requested_to_speak_at)
        
        # self_deaf
        hash_value ^= self.self_deaf << 3
        
        # self_mute
        hash_value ^= self.self_mute << 4
        
        # self_stream
        hash_value ^= self.self_stream << 5
        
        # self_video
        hash_value ^= self.self_video << 6
        
        # session_id
        hash_value ^= hash(self.session_id)
        
        # speaker
        hash_value ^= self.speaker << 1
        
        
        # user_id
        hash_value ^= self.user_id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the voice state.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        # Construct
        new = object.__new__(type(self))
        new._cache_user = None
        new.channel_id = self.channel_id
        new.deaf = self.deaf
        new.guild_id = self.guild_id
        new.mute = self.mute
        new.requested_to_speak_at = self.requested_to_speak_at
        new.self_deaf = self.self_deaf
        new.self_mute = self.self_mute
        new.self_stream = self.self_stream
        new.self_video = self.self_video
        new.session_id = self.session_id
        new.speaker = self.speaker
        new.user_id = self.user_id
        return new
    
    
    def copy_with(
        self,
        *,
        channel_id = ...,
        deaf = ...,
        guild_id = ...,
        speaker = ...,
        mute = ...,
        requested_to_speak_at = ...,
        self_deaf = ...,
        self_mute = ...,
        self_stream = ...,
        self_video = ...,
        session_id = ...,
        user_id = ...,
    ):
        """
        Copies the voice state with the given fields.
        
        Parameters
        ----------
        channel_id : `int`, Optional (Keyword only)
            The channel's identifier to where the user is connected to.
        deaf : `bool`, Optional (Keyword only)
            Whether the user is deafen.
        guild_id : `int`, Optional (Keyword only)
            The guild's identifier where the user is connected to.
        mute : `bool`, Optional (Keyword only)
            Whether the user is muted.
        requested_to_speak_at : `None`, `datetime`, Optional (Keyword only)
            When the user requested to speak.
        self_deaf : `bool`, Optional (Keyword only)
            Whether the user muted everyone else.
        self_mute : `bool`, Optional (Keyword only)
            Whether the user muted itself.
        self_stream : `bool`, Optional (Keyword only)
            Whether the user screen shares with the go live option.
        self_video : `bool`, Optional (Keyword only)
            Whether the user sends video from a camera source.
        session_id : `str``, Optional (Keyword only)
            The user's voice session id.
        speaker : `bool`, Optional (Keyword only)
            Whether the user is suppressed inside of the voice channel.
        user_id : `int`, Optional (Keyword only)
            The voice state's respective user's identifier.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = self.channel_id
        else:
            channel_id = validate_channel_id(channel_id)
        
        # deaf
        if deaf is ...:
            deaf = self.deaf
        else:
            deaf = validate_deaf(deaf)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # mute
        if mute is ...:
            mute = self.mute
        else:
            mute = validate_mute(mute)
        
        # requested_to_speak_at
        if requested_to_speak_at is ...:
            requested_to_speak_at = self.requested_to_speak_at
        else:
            requested_to_speak_at = validate_requested_to_speak_at(requested_to_speak_at)
        
        # self_deaf
        if self_deaf is ...:
            self_deaf = self.self_deaf
        else:
            self_deaf = validate_self_deaf(self_deaf)
        
        # self_mute
        if self_mute is ...:
            self_mute = self.self_mute
        else:
            self_mute = validate_self_mute(self_mute)
        
        # self_stream
        if self_stream is ...:
            self_stream = self.self_stream
        else:
            self_stream = validate_self_stream(self_stream)
        
        # self_video
        if self_video is ...:
            self_video = self.self_video
        else:
            self_video = validate_self_video(self_video)
        
        # session_id
        if session_id is ...:
            session_id = self.session_id
        else:
            session_id = validate_session_id(session_id)
        
        # speaker
        if speaker is ...:
            speaker = self.speaker
        else:
            speaker = validate_speaker(speaker)
        
        # user_id
        if user_id is ...:
            user_id = self.user_id
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        new = object.__new__(type(self))
        new._cache_user = None
        new.channel_id = channel_id
        new.deaf = deaf
        new.guild_id = guild_id
        new.mute = mute
        new.requested_to_speak_at = requested_to_speak_at
        new.self_deaf = self_deaf
        new.self_mute = self_mute
        new.self_stream = self_stream
        new.self_video = self_video
        new.session_id = session_id
        new.speaker = speaker
        new.user_id = user_id
        return new
    
    
    @property
    def user(self):
        """
        Returns the voice state's user.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        user = self._cache_user
        if (user is None):
            user = create_partial_user_from_id(self.user_id)
            self._cache_user = user
        
        return user
    
    
    def _set_cache_user(self, user):
        """
        Sets the cached user of the voice state.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The respective user of the voice state.
        """
        self._cache_user = user
    
    
    @property
    def channel(self):
        """
        Returns the voice state's channel, where the user is connected to.
        
        Returns
        -------
        channel : ``Channel``
        """
        return create_partial_channel_from_id(self.channel_id, ChannelType.unknown, self.guild_id)
    
    
    @property
    def guild(self):
        """
        Returns the voice state's respective guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        return GUILDS.get(self.guild_id, None)
    
    
    @property
    def is_speaker(self):
        """
        Deprecated and will be removed in 2023 Jul. Please use ``.speaker`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.is_speaker` is deprecated and will be removed in 2023 jul. '
                f'Please use `.speaker` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.speaker
