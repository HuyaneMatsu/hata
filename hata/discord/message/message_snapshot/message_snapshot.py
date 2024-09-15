__all__ = ('MessageSnapshot', )

from scarletio import RichAttributeErrorBaseType, export

from ...bases import id_sort_key
from ...core import CHANNELS
from ...role import create_partial_role_from_id
from ...utils import CHANNEL_MENTION_RP, DATETIME_FORMAT_CODE, DISCORD_EPOCH_START

from ..message import MessageFlag, MessageType
from ..message.constants import MESSAGE_STATE_MASK_CACHE_MENTIONED_CHANNELS

from .fields import (
    parse_attachments, parse_content, parse_created_at, parse_edited_at, parse_embeds, parse_flags,
    parse_mentioned_role_ids, parse_mentioned_users, parse_type, put_attachments_into, put_content_into,
    put_created_at_into, put_edited_at_into, put_embeds_into, put_flags_into, put_mentioned_role_ids_into,
    put_mentioned_users_into, put_type_into, validate_attachments, validate_content, validate_created_at,
    validate_edited_at, validate_embeds, validate_flags, validate_mentioned_role_ids, validate_mentioned_users,
    validate_type
)


@export
class MessageSnapshot(RichAttributeErrorBaseType):
    """
    Might be sent with a ``Message``, if it has rich presence-related chat embeds.
    
    Attributes
    ----------
    _cache_mentioned_channels : `None`, `tuple` of ``Channel``
        Mentioned channels by the message. Parsed from ``.content``. Defaults to `None`.
        
        Cache field used by ``.mentioned_channels``.
    
    _state : `int`
        Bitwise mask used to track the message's state.
    
    attachments : `None | tuple<Attachment>`
        The snapshotted message's attachments.
    
    content : `None | str`
        The snapshotted message's content.
    
    created_at : `DateTime`
        When the snapshotted message was created.
    
    edited_at : `None | Datetime`
        When the snapshotted message was edited.
    
    embeds : `None | tuple<Embed>`
        The snapshotted message's embeds.
    
    flags : ``MessageFlag``
        The snapshotted message's flags.
    
    mentioned_role_ids : `None | tuple<int>`
        The mentioned roles' identifiers.
    
    mentioned_users : `None | tuple<ClientUserBase>`
        The mentioned users.
    
    type : ``MessageType``
        The snapshotted message's type.
    """
    __slots__ = (
        '_cache_mentioned_channels', '_state', 'attachments', 'content', 'created_at', 'edited_at', 'embeds', 'flags',
        'mentioned_role_ids', 'mentioned_users', 'type'
    )
    
    def __new__(
        cls,
        *,
        attachments = ...,
        content = ...,
        created_at = ...,
        edited_at = ...,
        embeds = ...,
        flags = ...,
        mentioned_role_ids = ...,
        mentioned_users = ...,
        message_type = ...,
    ):
        """
        Creates a new message snapshot from the given parameters.
        
        Parameters
        ----------
        attachments : `None | iterable<Attachment>`, Optional (Keyword only)
            The snapshotted message's attachments.
        
        content : `None | str`, Optional (Keyword only)
            The snapshotted message's content.
        
        created_at : `DateTime`, Optional (Keyword only)
            When the snapshotted message was created.
        
        edited_at : `None | Datetime`, Optional (Keyword only)
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
        self.content = content
        self.created_at = created_at
        self.edited_at = edited_at
        self.embeds = embeds
        self.flags = flags
        self.mentioned_role_ids = mentioned_role_ids
        self.mentioned_users = mentioned_users
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
        self.content = parse_content(data)
        self.created_at = parse_created_at(data)
        self.edited_at = parse_edited_at(data)
        self.embeds = parse_embeds(data)
        self.flags = parse_flags(data)
        self.mentioned_role_ids = parse_mentioned_role_ids(data)
        self.mentioned_users = parse_mentioned_users(data, guild_id)
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
        put_attachments_into(self.attachments, data, defaults)
        put_content_into(self.content, data, defaults)
        put_created_at_into(self.created_at, data, defaults)
        put_edited_at_into(self.edited_at, data, defaults)
        put_embeds_into(self.embeds, data, defaults)
        put_flags_into(self.flags, data, defaults)
        put_mentioned_role_ids_into(self.mentioned_role_ids, data, defaults)
        put_mentioned_users_into(self.mentioned_users, data, defaults, guild_id = guild_id)
        put_type_into(self.type, data, defaults)
        return data
    
    
    def __eq__(self, other):
        """Returns whether the two message activities are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # attachments
        if self.attachments != other.attachments:
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
        
        new.type = self.type
        
        return new
    
    
    def copy_with(
        self,
        *,
        attachments = ...,
        content = ...,
        created_at = ...,
        edited_at = ...,
        embeds = ...,
        flags = ...,
        mentioned_role_ids = ...,
        mentioned_users = ...,
        message_type = ...,
    ):
        """
        Copies the message snapshot with the given fields.
        
        Parameters
        ----------
        attachments : `None | iterable<Attachment>`, Optional (Keyword only)
            The snapshotted message's attachments.
        content : `None | str`, Optional (Keyword only)
            The snapshotted message's content.
        created_at : `DateTime`, Optional (Keyword only)
            When the snapshotted message was created.
        edited_at : `None | Datetime`, Optional (Keyword only)
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
        new.content = content
        new.created_at = created_at
        new.edited_at = edited_at
        new.embeds = embeds
        new.flags = flags
        new.mentioned_role_ids = mentioned_role_ids
        new.mentioned_users = mentioned_users
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
        channel_mentions : `None`, `tuple` of ``Channel``
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
        mentioned_channels : `None`, `tuple` of ``Channel``
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
