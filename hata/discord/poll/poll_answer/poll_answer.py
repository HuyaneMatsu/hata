__all__ = ('PollAnswer',)

from ...bases import DiscordEntity
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...utils import sanitize_mentions

from .fields import (
    parse_emoji, parse_id, parse_text, put_emoji_into, put_id_into, put_text_into, validate_emoji, validate_id,
    validate_text
)


PRECREATE_FIELDS = {
    'emoji': ('emoji', validate_emoji),
    'text': ('text', validate_text),
}


class PollAnswer(DiscordEntity):
    """
    Represents a poll's answer.
    
    Attributes
    ----------
    emoji : `None`, ``Emoji``
        The poll answer's emoji.
    id : `int`
        The answer's identifier.
    text : `None`, `str`
        The poll answer's text.
    """
    __slots__ = ('emoji', 'text',)
    
    def __new__(cls, *, emoji = ..., text = ...):
        """
        Creates a new poll answer with the given parameters.
        
        Parameters
        ----------
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The answer's emoji.
        text : `None`, `str`, Optional (Keyword only)
            The answer's text.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # emoji
        if emoji is ...:
            emoji = None
        else:
            emoji = validate_emoji(emoji)
        
        # text
        if text is ...:
            text = None
        else:
            text = validate_text(text)
        
        self = object.__new__(cls)
        self.emoji = emoji
        self.id = 0
        self.text = text
        return self
    
    
    def __len__(self):
        """Returns the poll answer's length."""
        length = 0
        
        # emoji
        # does not count
        
        # id
        # does not count
        
        # text
        text = self.text
        if (text is not None):
            length += len(text)
        
        return length
    
    
    def __bool__(self):
        """Returns whether the poll answer has any fields set."""
        # emoji
        if self.emoji is not None:
            return True
        
        # id
        # does not count
        
        # text
        if self.text is not None:
            return True
        
        return False
    
    
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # id
        answer_id = self.id
        if answer_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(answer_id))
            
            field_added = True
        else:
            field_added = False
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' emoji = ')
            repr_parts.append(repr(emoji))
        
        # text
        text = self.text
        if (text is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' text = ')
            repr_parts.append(repr(text))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the poll answer's hash value."""
        hash_value = 0
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= hash(emoji)
        
        # id
        hash_value ^= self.id
        
        # text
        text = self.text
        if (text is not None):
            hash_value ^= hash(text)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two poll answers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # id
        self_id = self.id
        other_id = other.id
        if (self_id and other_id) and (self_id != other_id):
            return False
        
        # emoji
        if self.emoji is not other.emoji:
            return False
        
        # text
        if self.text != other.text:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new poll answer instance from the given json data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to create poll answer from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.emoji = parse_emoji(data)
        self.id = parse_id(data)
        self.text = parse_text(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Returns the poll answer as a json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_emoji_into(self.emoji, data, defaults)
        put_text_into(self.text, data, defaults)
        
        if include_internals:
            put_id_into(self.id, data, defaults)
        
        return data
    
    
    def clean_copy(self, guild = None):
        """
        Creates a clean copy of the poll answer by removing the mentions in it's contents.
        
        Parameters
        ----------
        guild : `None`, ``Guild`` = `None`, Optional
            The respective guild as a context to look up guild specific names of entities.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.emoji = self.emoji
        new.id = 0
        new.text = sanitize_mentions(self.text, guild)
        return new
    
    
    def copy(self):
        """
        Copies the poll answer.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.emoji = self.emoji
        new.id = 0
        new.text = self.text
        return new
    
    
    def copy_with(self, *, emoji = ..., text = ...):
        """
        Copies the poll answer with the given parameters.
        
        Parameters
        ----------
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The answer's emoji.
        text : `None`, `str`, Optional (Keyword only)
            The answer's text.
        
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
        # emoji
        if emoji is ...:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # text
        if text is ...:
            text = self.text
        else:
            text = validate_text(text)
        
        new = object.__new__(type(self))
        new.emoji = emoji
        new.id = 0
        new.text = text
        return new
    
    
    @classmethod
    def precreate(
        cls,
        answer_id,
        **keyword_parameters,
    ):
        """
        Precreates an answer. Since answers are not cached, this method just a ``.__new__`` alternative.
        
        Parameters
        ----------
        answer_id : `int`
            The answer's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional parameters defining how the answer's fields should be set.
        
        Other Parameters
        ----------------
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The answer's emoji.
        text : `None`, `str`, Optional (Keyword only)
            The answer's text.
        
        Returns
        -------
        self : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        answer_id = validate_id(answer_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        
        else:
            processed = None
        
        # Construct
        
        self = object.__new__(cls)
        self.emoji = None
        self.id = answer_id
        self.text = None
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self

    
    @property
    def contents(self):
        """
        Returns the contents of the poll answer.
        
        Returns
        -------
        contents : `list<str>`
        """
        return [*self.iter_contents()]
    
    
    def iter_contents(self):
        """
        Iterates over the contents of the poll answer.
        
        This method is an iterable generator.
        
        Yields
        ------
        content : `str`
        """
        text = self.text
        if (text is not None):
            yield text
