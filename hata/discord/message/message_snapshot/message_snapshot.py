__all__ = ('MessageSnapshot', )

from scarletio import RichAttributeErrorBaseType, export

from ...bases import id_sort_key
from ...core import CHANNELS
from ...role import create_partial_role_from_id
from ...utils import CHANNEL_MENTION_RP, DATETIME_FORMAT_CODE, DISCORD_EPOCH_START

from ..message import MessageFlag, MessageType
from ..message.constants import MESSAGE_STATE_MASK_CACHE_MENTIONED_CHANNELS

from .fields import (
    parse_attachments, parse_components, parse_content, parse_created_at, parse_edited_at, parse_embeds, parse_flags,
    parse_mentioned_role_ids, parse_mentioned_users, parse_soundboard_sounds, parse_stickers, parse_type,
    put_attachments, put_components, put_content, put_created_at, put_edited_at,
    put_embeds, put_flags, put_mentioned_role_ids, put_mentioned_users, put_soundboard_sounds,
    put_stickers, put_type, validate_attachments, validate_components, validate_content, validate_created_at,
    validate_edited_at, validate_embeds, validate_flags, validate_mentioned_role_ids, validate_mentioned_users,
    validate_soundboard_sounds, validate_stickers, validate_type
)


@export
class MessageSnapshot(RichAttributeErrorBaseType):
    """
    Might be sent with a ``Message``, if it has rich presence-related chat embeds.
    
    Attributes
    ----------
    _cache_mentioned_channels : ``None | tuple<Channel>``
        Mentioned channels by the message. Parsed from ``.content``. Defaults to `None`.
        
        Cache field used by ``.mentioned_channels``.
    
    _state : `int`
        Bitwise mask used to track the message's state.
    
    attachments : ``None | tuple<Attachment>``
        The snapshotted message's attachments.
    
    components : ``None | tuple<Component>``
        The snapshotted message's components.
    
    content : `None | str`
        The snapshotted message's content.
    
    created_at : `DateTime`
        When the snapshotted message was created.
    
    edited_at : `None | DateTime`
        When the snapshotted message was edited.
    
    embeds : ``None | tuple<Embed>``
        The snapshotted message's embeds.
    
    flags : ``MessageFlag``
        The snapshotted message's flags.
    
    mentioned_role_ids : `None | tuple<int>`
        The mentioned roles' identifiers.
    
    mentioned_users : ``None | tuple<ClientUserBase>``
        The mentioned users.
    
    soundboard_sounds : ``None | tuple<SoundboardSound>``
        The soundboard sounds attached to the message. 
    
    stickers : `None | tuple<Sticker>`
        The snapshotted message's stickers.
    
    type : ``MessageType``
        The snapshotted message's type.
    """
    __slots__ = (
        '_cache_mentioned_channels', '_state', 'attachments', 'components', 'content', 'created_at', 'edited_at',
        'embeds', 'flags', 'mentioned_role_ids', 'mentioned_users', 'soundboard_sounds', 'stickers', 'type'
    )
    
    def __new__(
        cls,
        *,
        attachments = ...,
        components = ...,
        content = ...,
        created_at = ...,
        edited_at = ...,
        embeds = ...,
        flags = ...,
        mentioned_role_ids = ...,
        mentioned_users = ...,
        message_type = ...,
        soundboard_sounds = ...,
        stickers = ...,
    ):
        """
        Creates a new message snapshot from the given parameters.
        
        Parameters
        ----------
        attachments : `None | iterable<Attachment>`, Optional (Keyword only)
            The snapshotted message's attachments.
        
        components : ``None | iterable<Component>``, Optional (Keyword only)
            The snapshotted message's components.
        
        content : `None | str`, Optional (Keyword only)
            The snapshotted message's content.
        
        created_at : `DateTime`, Optional (Keyword only)
            When the snapshotted message was created.
        
        edited_at : `None | DateTime`, Optional (Keyword only)
            When the snapshotted message was edited.
        
        embeds : `None | iterable<Embed>`, Optional (Keyword only)
            The snapshotted message's embeds.
        
        flags : `MessageFlag | int | None`, Optional (Keyword only)
            The snapshotted message's flags.
        
        mentioned_role_ids : `None | iterable<int>` | iterable<Role>`, Optional (Keyword only)
            The mentioned roles' identifiers.
        
        mentioned_users : `None | iterable<ClientUserBase>`, Optional (Keyword only)
            The mentioned users.
        
        message_type : `MessageType | int | None`, Optional (Keyword only)
            The snapshotted message's type.
        
        soundboard_sounds : `None | iterable<SoundboardSound>`, Optional (Keyword only)
            Soundboard sounds attached to the message.
        
        stickers : `None | iterable<Sticker>`, Optional (Keyword only)
            The snapshotted message's stickers.
        
        Raises
        ------
        TypeError
            - If a parameter's content is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # attachments
        if attachments is ...:
            attachments = None
        else:
            attachments = validate_attachments(attachments)
        
        # components
        if components is ...:
            components = None
        else:
            components = validate_components(components)
        
        # content
        if content is ...:
            content = None
        else:
            content = validate_content(content)
        
        # created_at
        if created_at is ...:
            created_at = DISCORD_EPOCH_START
        else:
            created_at = validate_created_at(created_at)
        
        # edited_at
        if edited_at is ...:
            edited_at = None
        else:
            edited_at = validate_edited_at(edited_at)
        
        # embeds
        if embeds is ...:
            embeds = None
        else:
            embeds = validate_embeds(embeds)
        
        # flags
        if flags is ...:
            flags = MessageFlag()
        else:
            flags = validate_flags(flags)
        
        # mentioned_role_ids
        if mentioned_role_ids is ...:
            mentioned_role_ids = None
        else:
            mentioned_role_ids = validate_mentioned_role_ids(mentioned_role_ids)
        
        # mentioned_users
        if mentioned_users is ...:
            mentioned_users = None
        else:
            mentioned_users = validate_mentioned_users(mentioned_users)
        
        # soundboard_sounds
        if soundboard_sounds is ...:
            soundboard_sounds = None
        else:
            soundboard_sounds = validate_soundboard_sounds(soundboard_sounds)
        
        # stickers
        if stickers is ...:
            stickers = None
        else:
            stickers = validate_stickers(stickers)
        
        # type
        if message_type is ...:
            message_type = MessageType.default
        else:
            message_type = validate_type(message_type)
        
        # Construct
        self = object.__new__(cls)
        self._cache_mentioned_channels = None
        self._state = 0
        self.attachments = attachments
        self.components = components
        self.content = content
        self.created_at = created_at
        self.edited_at = edited_at
        self.embeds = embeds
        self.flags = flags
        self.mentioned_role_ids = mentioned_role_ids
        self.mentioned_users = mentioned_users
        self.soundboard_sounds = soundboard_sounds
        self.stickers = stickers
        self.type = message_type
        return self
    
    
    @classmethod
    def from_data(cls, data, guild_id = 0):
        """
        Creates a new message snapshot from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Message snapshot data.
        guild_id : `int` = `0`, Optional
            The respective guild's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._cache_mentioned_channels = None
        self._state = 0
        self.attachments = parse_attachments(data)
        self.components = parse_components(data)
        self.content = parse_content(data)
        self.created_at = parse_created_at(data)
        self.edited_at = parse_edited_at(data)
        self.embeds = parse_embeds(data)
        self.flags = parse_flags(data)
        self.mentioned_role_ids = parse_mentioned_role_ids(data)
        self.mentioned_users = parse_mentioned_users(data, guild_id)
        self.soundboard_sounds = parse_soundboard_sounds(data)
        self.stickers = parse_stickers(data)
        self.type = parse_type(data)
        return self
    
    
    def to_data(self, *, defaults = False, guild_id = 0):
        """
        Converts the message snapshot back to json a serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        guild_id : `int` = `0`, Optional (Keyword only)
            The respective guild's identifier.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_attachments(self.attachments, data, defaults)
        put_components(self.components, data, defaults)
        put_content(self.content, data, defaults)
        put_created_at(self.created_at, data, defaults)
        put_edited_at(self.edited_at, data, defaults)
        put_embeds(self.embeds, data, defaults)
        put_flags(self.flags, data, defaults)
        put_mentioned_role_ids(self.mentioned_role_ids, data, defaults)
        put_mentioned_users(self.mentioned_users, data, defaults, guild_id = guild_id)
        put_soundboard_sounds(self.soundboard_sounds, data, defaults)
        put_stickers(self.stickers, data, defaults)
        put_type(self.type, data, defaults)
        return data
    
    
    def __eq__(self, other):
        """Returns whether the two message activities are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # attachments
        if self.attachments != other.attachments:
            return False
        
        # components
        if self.components != other.components:
            return False
        
        # content
        if self.content != other.content:
            return False
        
        # created_at
        if self.created_at != other.created_at:
            return False
        
        # edited_at
        if self.edited_at != other.edited_at:
            return False
        
        # embeds
        if self.embeds != other.embeds:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        # mentioned_role_ids
        if self.mentioned_role_ids != other.mentioned_role_ids:
            return False
        
        # mentioned_users
        if self.mentioned_users != other.mentioned_users:
            return False
        
        # soundboard_sounds
        if self.soundboard_sounds != other.soundboard_sounds:
            return False
        
        # stickers
        if self.stickers != other.stickers:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns the message snapshot's representation."""
        repr_parts = ['<', type(self).__name__]
        
        field_added = False
        
        # attachments
        attachments = self.attachments
        if (attachments is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' attachments = ')
            repr_parts.append(repr(attachments))
        
        # components
        components = self.components
        if (components is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' components = ')
            repr_parts.append(repr(components))
        
        # content
        content = self.content
        if (content is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' content = ')
            repr_parts.append(repr(content))
        
        # created_at
        created_at = self.created_at
        if (created_at != DISCORD_EPOCH_START):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' created_at = ')
            repr_parts.append(format(created_at, DATETIME_FORMAT_CODE))
        
        # edited_at
        edited_at = self.edited_at
        if (edited_at is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' edited_at = ')
            repr_parts.append(format(edited_at, DATETIME_FORMAT_CODE))
        
        # embeds
        embeds = self.embeds
        if (embeds is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' embeds = ')
            repr_parts.append(repr(embeds))
        
        # flags
        flags = self.flags
        if flags:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' flags = ')
            repr_parts.append(repr(flags))
        
        # mentioned_role_ids
        mentioned_role_ids = self.mentioned_role_ids
        if mentioned_role_ids:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' mentioned_role_ids = ')
            repr_parts.append(repr(mentioned_role_ids))
        
        # mentioned_users
        mentioned_users = self.mentioned_users
        if mentioned_users:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' mentioned_users = ')
            repr_parts.append(repr(mentioned_users))
        
        # soundboard_sounds
        soundboard_sounds = self.soundboard_sounds
        if (soundboard_sounds is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' soundboard_sounds = ')
            repr_parts.append(repr(soundboard_sounds))
        
        # stickers
        stickers = self.stickers
        if (stickers is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' stickers = ')
            repr_parts.append(repr(stickers))
        
        # type
        message_type = self.type
        if (message_type is not MessageType.default):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' type = ')
            repr_parts.append(message_type.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(message_type.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the message snapshot's hash value."""
        hash_value = 0
        
        # attachments
        attachments = self.attachments
        if (attachments is not None):
            hash_value ^= len(attachments)
            
            for attachment in attachments:
                hash_value ^= hash(attachment)
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components)
            
            for attachment in components:
                hash_value ^= hash(attachment)
        
        # content
        content = self.content
        if (content is not None):
            hash_value ^= hash(content)
        
        # created_at
        created_at = self.created_at
        if (created_at != DISCORD_EPOCH_START):
            hash_value ^= hash(created_at)
        
        # edited_at
        edited_at = self.edited_at
        if (edited_at is not None):
            hash_value ^= hash(edited_at)
        
        # embeds
        embeds = self.embeds
        if (embeds is not None):
            hash_value ^= len(embeds) << 8
            
            for embed in embeds:
                hash_value ^= hash(embed)
        
        # flags
        hash_value ^= self.flags
        
        # mentioned_role_ids
        mentioned_role_ids = self.mentioned_role_ids
        if (mentioned_role_ids is not None):
            hash_value ^= len(mentioned_role_ids) << 21
            
            for role_id in mentioned_role_ids:
                hash_value ^= role_id
        
        # mentioned_users
        mentioned_users = self.mentioned_users
        if (mentioned_users is not None):
            hash_value ^= len(mentioned_users) << 25
            
            for user in mentioned_users:
                hash_value ^= hash(user)
        
        # soundboard_sounds
        soundboard_sounds = self.soundboard_sounds
        if (soundboard_sounds is not None):
            hash_value ^= len(soundboard_sounds) << 27
            
            for soundboard_sound in soundboard_sounds:
                hash_value ^= hash(soundboard_sound)
        
        # stickers
        stickers = self.stickers
        if (stickers is not None):
            hash_value ^= len(stickers)
            
            for attachment in stickers:
                hash_value ^= hash(attachment)
        
        # type
        hash_value ^= hash(self.type)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the message snapshot.
        
        Returns
        -------
        new : `instance<content<self>>`
        """
        new = object.__new__(type(self))
        new._cache_mentioned_channels = None
        new._state = 0
        
        attachments = self.attachments
        if (attachments is not None):
            attachments = (*attachments,)
        new.attachments = attachments
        
        components = self.components
        if (components is not None):
            components = (*components,)
        new.components = components
        
        new.content = self.content
        new.created_at = self.created_at
        new.edited_at = self.edited_at
        
        embeds = self.embeds
        if (embeds is not None):
            embeds = (*(embed.copy() for embed in embeds),)
        new.embeds = embeds
        
        new.flags = self.flags
        
        mentioned_role_ids = self.mentioned_role_ids
        if (mentioned_role_ids is not None):
            mentioned_role_ids = (*mentioned_role_ids,)
        new.mentioned_role_ids = mentioned_role_ids
        
        mentioned_users = self.mentioned_users
        if (mentioned_users is not None):
            mentioned_users = (*mentioned_users,)
        new.mentioned_users = mentioned_users
        
        soundboard_sounds = self.soundboard_sounds
        if (soundboard_sounds is not None):
            soundboard_sounds = (*soundboard_sounds,)
        new.soundboard_sounds = soundboard_sounds
        
        stickers = self.stickers
        if (stickers is not None):
            stickers = (*stickers,)
        new.stickers = stickers
        
        new.type = self.type
        
        return new
    
    
    def copy_with(
        self,
        *,
        attachments = ...,
        components = ...,
        content = ...,
        created_at = ...,
        edited_at = ...,
        embeds = ...,
        flags = ...,
        mentioned_role_ids = ...,
        mentioned_users = ...,
        message_type = ...,
        soundboard_sounds = ...,
        stickers = ...,
    ):
        """
        Copies the message snapshot with the given fields.
        
        Parameters
        ----------
        attachments : `None | iterable<Attachment>`, Optional (Keyword only)
            The snapshotted message's attachments.
        
        components : ``None | iterable<Component>``, Optional (Keyword only)
            The snapshotted message's components.
        
        content : `None | str`, Optional (Keyword only)
            The snapshotted message's content.
        
        created_at : `DateTime`, Optional (Keyword only)
            When the snapshotted message was created.
        
        edited_at : `None | DateTime`, Optional (Keyword only)
            When the snapshotted message was edited.
        
        embeds : `None | iterable<Embed>`, Optional (Keyword only)
            The snapshotted message's embeds.
        
        flags : `MessageFlag | int | None`, Optional (Keyword only)
            The snapshotted message's flags.
        
        mentioned_role_ids : `None | iterable<int>` | iterable<Role>`, Optional (Keyword only)
            The mentioned roles' identifiers.
        
        mentioned_users : `None | iterable<ClientUserBase>`, Optional (Keyword only)
            The mentioned users.
        
        message_type : `MessageType | int | None`, Optional (Keyword only)
            The snapshotted message's type.
        
        soundboard_sounds : `None | iterable<SoundboardSound>`, Optional (Keyword only)
            Soundboard sounds attached to the message.
        
        stickers : `None | iterable<Sticker>`, Optional (Keyword only)
            The snapshotted message's stickers.
        
        Returns
        -------
        new : `instance<content<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's content is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # attachments
        if attachments is ...:
            attachments = self.attachments
            if (attachments is not None):
                attachments = (*attachments,)
        else:
            attachments = validate_attachments(attachments)
        
        # components
        if components is ...:
            components = self.components
            if (components is not None):
                components = (*components,)
        else:
            components = validate_components(components)
        
        # content
        if content is ...:
            content = self.content
        else:
            content = validate_content(content)
        
        # created_at
        if created_at is ...:
            created_at = self.created_at
        else:
            created_at = validate_created_at(created_at)
        
        # edited_at
        if edited_at is ...:
            edited_at = self.edited_at
        else:
            edited_at = validate_edited_at(edited_at)
        
        # embeds
        if embeds is ...:
            embeds = self.embeds
            if (embeds is not None):
                embeds = (*(embed.copy() for embed in embeds),)
        else:
            embeds = validate_embeds(embeds)
        
        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
        # mentioned_role_ids
        if mentioned_role_ids is ...:
            mentioned_role_ids = self.mentioned_role_ids
            if (mentioned_role_ids is not None):
                mentioned_role_ids = (*mentioned_role_ids,)
        else:
            mentioned_role_ids = validate_mentioned_role_ids(mentioned_role_ids)
        
        # mentioned_users
        if mentioned_users is ...:
            mentioned_users = self.mentioned_users
            if (mentioned_users is not None):
                mentioned_users = (*mentioned_users,)
        else:
            mentioned_users = validate_mentioned_users(mentioned_users)
        
        # soundboard_sounds
        if soundboard_sounds is ...:
            soundboard_sounds = self.soundboard_sounds
            if (soundboard_sounds is not None):
                soundboard_sounds = (*soundboard_sounds,)
        else:
            soundboard_sounds = validate_soundboard_sounds(soundboard_sounds)
        
        # stickers
        if stickers is ...:
            stickers = self.stickers
            if (stickers is not None):
                stickers = (*stickers,)
        else:
            stickers = validate_stickers(stickers)
        
        # type
        if message_type is ...:
            message_type = self.type
        else:
            message_type = validate_type(message_type)
        
        # Construct
        new = object.__new__(type(self))
        new._cache_mentioned_channels = None
        new._state = 0
        new.attachments = attachments
        new.components = components
        new.content = content
        new.created_at = created_at
        new.edited_at = edited_at
        new.embeds = embeds
        new.flags = flags
        new.mentioned_role_ids = mentioned_role_ids
        new.mentioned_users = mentioned_users
        new.soundboard_sounds = soundboard_sounds
        new.stickers = stickers
        new.type = message_type
        return new
    
    # Iterators
    
    def iter_attachments(self):
        """
        Iterates over the attachments of the message snapshot.
        
        This method is an iterable generator.
        
        Yields
        ------
        attachment : ``Attachment``
        """
        attachments = self.attachments
        if attachments is not None:
            yield from attachments
    
    
    def iter_components(self):
        """
        Iterates over the components of the message snapshot.
        
        This method is an iterable generator.
        
        Yields
        ------
        attachment : ``Component``
        """
        components = self.components
        if components is not None:
            yield from components
    
    
    def iter_embeds(self):
        """
        Iterates over the embeds of the message snapshot.
        
        This method is an iterable generator.
        
        Yields
        ------
        embed : ``Embed``
        """
        embeds = self.embeds
        if embeds is not None:
            yield from embeds
    
    
    def iter_mentioned_role_ids(self):
        """
        Iterates over the mentioned roles' identifiers in the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        mentioned_role_id : `int`
        """
        mentioned_role_ids = self.mentioned_role_ids
        if (mentioned_role_ids is not None):
            yield from mentioned_role_ids
    
    
    def iter_mentioned_roles(self):
        """
        Iterates over the mentioned roles in the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        mentioned_role : ``Role``
        """
        mentioned_role_ids = self.mentioned_role_ids
        if (mentioned_role_ids is not None):
            for role_id in mentioned_role_ids:
                yield create_partial_role_from_id(role_id)
    
    
    def iter_mentioned_users(self):
        """
        Iterates over the mentioned users in the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        mentioned_user : ``ClientUserBase``
        """
        mentioned_users = self.mentioned_users
        if (mentioned_users is not None):
            yield from mentioned_users
    
    
    def iter_mentioned_channels(self):
        """
        Iterates over the mentioned channels in the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        mentioned_channel : ``Channel``
        """
        mentioned_channels = self.mentioned_channels
        if (mentioned_channels is not None):
            yield from mentioned_channels
    
    
    def iter_soundboard_sounds(self):
        """
        Iterates over the soundboard sounds of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        soundboard_sounds : ``SoundboardSound``
        """
        soundboard_sounds = self.soundboard_sounds
        if (soundboard_sounds is not None):
            yield from soundboard_sounds
    
    
    def iter_stickers(self):
        """
        Iterates over the stickers of the message snapshot.
        
        This method is an iterable generator.
        
        Yields
        ------
        attachment : ``Sticker``
        """
        stickers = self.stickers
        if stickers is not None:
            yield from stickers
    
    
    # get many
    
    
    @property
    def mentioned_roles(self):
        """
        The mentioned roles by the message. If there is non, returns `None`.
        
        Returns
        -------
        role_mentions : `None | tuple<Role>`
        """
        mentioned_role_ids = self.mentioned_role_ids
        if (mentioned_role_ids is not None):
            return (*(create_partial_role_from_id(role_id) for role_id in mentioned_role_ids),)
    
    
    
    def _get_mentioned_channels(self):
        """
        Looks up the ``.contents`` of the message and searches channel mentions in them.
        
        Invalid channel mentions are ignored.
        
        Returns
        -------
        channel_mentions : ``None | tuple<Channel>``
            The parsed channel mentions.
        """
        mentioned_channels = None
        
        content = self.content
        if content is None:
            return mentioned_channels
        
        for channel_id in CHANNEL_MENTION_RP.findall(content):
            channel_id = int(channel_id)
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                continue
            
            if mentioned_channels is None:
                mentioned_channels = set()
            
            mentioned_channels.add(channel)
        
        if mentioned_channels is not None:
            mentioned_channels = tuple(sorted(mentioned_channels, key = id_sort_key))
        
        return mentioned_channels
    
    
    @property
    def mentioned_channels(self):
        """
        The mentioned channels by the message. If there is non returns `None`.
        
        Returns
        -------
        mentioned_channels : ``None | tuple<Channel>``
        """
        state = self._state
        if state & MESSAGE_STATE_MASK_CACHE_MENTIONED_CHANNELS:
            mentioned_channels = self._cache_mentioned_channels
        else:
            mentioned_channels = self._get_mentioned_channels()
            self._cache_mentioned_channels = mentioned_channels
            self._state = state | MESSAGE_STATE_MASK_CACHE_MENTIONED_CHANNELS
        
        return mentioned_channels
    
    # get one
    
    @property
    def attachment(self):
        """
        Returns the first attachment in the message snapshot.

        Returns
        -------
        attachment : `None | Attachment`
        """
        attachments = self.attachments
        if attachments is not None:
            return attachments[0]
    
    
    @property
    def embed(self):
        """
        Returns the first embed in the message snapshot.

        Returns
        -------
        embed : `None | Embed`
        """
        embeds = self.embeds
        if embeds is not None:
            return embeds[0]
    
    
    @property
    def soundboard_sound(self):
        """
        Returns the message's first soundboard sound.
        
        Returns
        -------
        soundboard_sound : ``None | SoundboardSound``
        """
        soundboard_sounds = self.soundboard_sounds
        if (soundboard_sounds is not None):
            return soundboard_sounds[0]
    
    
    @property
    def sticker(self):
        """
        Returns the first sticker in the message snapshot.

        Returns
        -------
        Sticker : `None | Sticker`
        """
        stickers = self.stickers
        if stickers is not None:
            return stickers[0]
