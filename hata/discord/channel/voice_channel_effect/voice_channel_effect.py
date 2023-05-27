__all__ = ('VoiceChannelEffect',)

from scarletio import copy_docs

from ...bases import EventBase
from ...core import GUILDS
from ...user import create_partial_user_from_id

from ..channel import ChannelType, create_partial_channel_from_id

from .fields import (
    parse_animation_id, parse_animation_type, parse_channel_id, parse_emoji, parse_guild_id, parse_user_id,
    put_animation_id_into, put_animation_type_into, put_channel_id_into, put_emoji_into, put_guild_id_into,
    put_user_id_into, validate_animation_id, validate_animation_type, validate_channel_id, validate_emoji,
    validate_guild_id, validate_user_id
)
from .preinstanced import VoiceChannelEffectAnimationType


class VoiceChannelEffect(EventBase):
    """
    Represents a voice channel effect sent to a voice channel.
    
    Attributes
    ----------
    animation_id : `int`
        The identifier of the animation of the voice channel effect.
    animation_type : ``VoiceChannelEffectAnimationType``
        The animation's type.
    channel_id : `int`
        The channel's identifier where the effect was sent.
    emoji : `None`, ``Emoji``
        The emoji sent.
    guild_id : `int`
        The guild's identifier where the event was sent.
    user_id : `int`
        The user's identifier who sent the effect.
    """
    __slots__ = ('animation_id', 'animation_type', 'channel_id', 'emoji', 'guild_id', 'user_id')
    
    def __new__(
        cls,
        *,
        animation_id = ...,
        animation_type = ...,
        channel_id = ...,
        emoji = ...,
        guild_id = ...,
        user_id = ...,
    ):
        """
        Creates a new voice channel effect event.
        
        Parameters
        ----------
        animation_id : `int`, Optional (Keyword only)
            The identifier of the animation of the voice channel effect.
        animation_type : ``VoiceChannelEffectAnimationType``, `int`, Optional (Keyword only)
            The animation's type.
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where the effect was sent.
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The emoji sent.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild or its identifier where the event was sent.
        user_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The user or its identifier who sent the effect.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # animation_id
        if animation_id is ...:
            animation_id = 0
        else:
            animation_id = validate_animation_id(animation_id)
        
        # animation_type
        if animation_type is ...:
            animation_type = VoiceChannelEffectAnimationType.premium
        else:
            animation_type = validate_animation_type(animation_type)
        
        # channel_id
        if channel_id is ...:
            channel_id = 0
        else:
            channel_id = validate_channel_id(channel_id)
        
        # emoji
        if emoji is ...:
            emoji = None
        else:
            emoji = validate_emoji(emoji)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # user_id
        if user_id is ...:
            user_id = 0
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        self = object.__new__(cls)
        self.animation_id = animation_id
        self.animation_type = animation_type
        self.channel_id = channel_id
        self.emoji = emoji
        self.guild_id = guild_id
        self.user_id = user_id
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a voice channel effect event from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Voice channel effect event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.animation_id = parse_animation_id(data)
        self.animation_type = parse_animation_type(data)
        self.channel_id = parse_channel_id(data)
        self.emoji = parse_emoji(data)
        self.guild_id = parse_guild_id(data)
        self.user_id = parse_user_id(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the voice channel effect event into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_animation_id_into(self.animation_id, data, defaults)
        put_animation_type_into(self.animation_type, data, defaults)
        put_emoji_into(self.emoji, data, defaults)
        
        if include_internals:
            put_channel_id_into(self.channel_id, data, defaults)
            put_guild_id_into(self.guild_id, data, defaults)
            put_user_id_into(self.user_id, data, defaults)
        
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', channel_id = ')
        repr_parts.append(repr(self.channel_id))
        
        repr_parts.append(', user_id = ')
        repr_parts.append(repr(self.user_id))
        
        animation_type = self.animation_type
        repr_parts.append(', animation_type = ')
        repr_parts.append(animation_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(animation_type.value))
        
        repr_parts.append(', animation_id = ')
        repr_parts.append(repr(self.animation_id))
        
        emoji = self.emoji
        if (emoji is not None):
            repr_parts.append(', emoji = ')
            repr_parts.append(repr(emoji))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 5
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.channel
        yield self.user
        yield self.animation_type
        yield self.animation_type
        yield self.emoji
        
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # animation_id
        if self.animation_id != other.animation_id:
            return False
        
        # animation_type
        if self.animation_type is not other.animation_type:
            return False
        
        # channel_id
        if self.channel_id is not other.channel_id:
            return False
        
        # emoji
        if self.emoji is not other.emoji:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # user_id
        if self.user_id != other.user_id:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # animation_id
        hash_value ^= hash(self.animation_id)
        
        # animation_type
        hash_value ^= hash(self.animation_type)
        
        # channel_id
        hash_value ^= self.channel_id
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= hash(emoji)
        
        # guild_id
        hash_value ^= self.guild_id
        
        # user_id
        hash_value ^= self.user_id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the voice channel effect event.
        
        Returns
        -------
        new : `instance<type<new>>`
        """
        new = object.__new__(type(self))
        new.animation_id = self.animation_id
        new.animation_type = self.animation_type
        new.channel_id = self.channel_id
        new.emoji = self.emoji
        new.guild_id = self.guild_id
        new.user_id = self.user_id
        return new
    
    
    def copy_with(
        self,
        *,
        animation_id = ...,
        animation_type = ...,
        channel_id = ...,
        emoji = ...,
        guild_id = ...,
        user_id = ...,
    ):
        """
        Copies new voice channel effect event with the given fields.
        
        Parameters
        ----------
        animation_id : `int`, Optional (Keyword only)
            The identifier of the animation of the voice channel effect.
        animation_type : ``VoiceChannelEffectAnimationType``, `int`, Optional (Keyword only)
            The animation's type.
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where the effect was sent.
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The emoji sent.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild or its identifier where the event was sent.
        user_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The user or its identifier who sent the effect.
        
        Returns
        -------
        new : `instance<type<new>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # animation_id
        if animation_id is ...:
            animation_id = self.animation_id
        else:
            animation_id = validate_animation_id(animation_id)
        
        # animation_type
        if animation_type is ...:
            animation_type = self.animation_type
        else:
            animation_type = validate_animation_type(animation_type)
        
        # channel_id
        if channel_id is ...:
            channel_id = self.channel_id
        else:
            channel_id = validate_channel_id(channel_id)
        
        # emoji
        if emoji is ...:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # user_id
        if user_id is ...:
            user_id = self.user_id
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        new = object.__new__(type(self))
        new.animation_id = animation_id
        new.animation_type = animation_type
        new.channel_id = channel_id
        new.emoji = emoji
        new.guild_id = guild_id
        new.user_id = user_id
        return new
    
    
    @property
    def channel(self):
        """
        Returns the voice channel effect event's channel.
        
        Returns
        -------
        channel : ``Channel``
        """
        return create_partial_channel_from_id(self.channel_id, ChannelType.guild_voice, self.guild_id)
    
    
    @property
    def guild(self):
        """
        Returns the voice channel effect's guild. If the guild is not cached returns `None`.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def user(self):
        """
        Returns the voice channel effect event's user.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        return create_partial_user_from_id(self.user_id)
