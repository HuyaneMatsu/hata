__all__ = ('MessageSnapshot', )

from scarletio import RichAttributeErrorBaseType, export

from ...core import GUILDS
from ...utils import DATETIME_FORMAT_CODE, DISCORD_EPOCH_START

from ..message import MessageFlag

from .fields import (
    parse_attachments, parse_content, parse_created_at, parse_edited_at, parse_embeds, parse_flags,
    put_attachments_into, put_content_into, put_created_at_into, put_edited_at_into, put_embeds_into, put_flags_into,
    validate_attachments, validate_content, validate_created_at, validate_edited_at, validate_embeds, validate_flags
)


@export
class MessageSnapshot(RichAttributeErrorBaseType):
    """
    Might be sent with a ``Message``, if it has rich presence-related chat embeds.
    
    Attributes
    ----------
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
    """
    __slots__ = ('attachments', 'content', 'created_at', 'edited_at', 'embeds', 'flags')
    
    def __new__(
        cls,
        *,
        attachments = ...,
        content = ...,
        created_at = ...,
        edited_at = ...,
        embeds = ...,
        flags = ...,
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
        
        # Construct
        self = object.__new__(cls)
        self.attachments = attachments
        self.content = content
        self.created_at = created_at
        self.edited_at = edited_at
        self.embeds = embeds
        self.flags = flags
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new message snapshot from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Message snapshot data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.attachments = parse_attachments(data)
        self.content = parse_content(data)
        self.created_at = parse_created_at(data)
        self.edited_at = parse_edited_at(data)
        self.embeds = parse_embeds(data)
        self.flags = parse_flags(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the message snapshot back to json a serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
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
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the message snapshot.
        
        Returns
        -------
        new : `instance<content<self>>`
        """
        new = object.__new__(type(self))
        
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
        
        # Construct
        new = object.__new__(type(self))
        new.attachments = attachments
        new.content = content
        new.created_at = created_at
        new.edited_at = edited_at
        new.embeds = embeds
        new.flags = flags
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
