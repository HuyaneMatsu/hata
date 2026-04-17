__all__ = ('PollQuestion',)

from scarletio import RichAttributeErrorBaseType

from ...utils import sanitize_mentions

from .fields import parse_text, put_text, validate_text


class PollQuestion(RichAttributeErrorBaseType):
    """
    Represents a poll's question.
    
    Attributes
    ----------
    text : `None`, `str`
        The poll question's text.
    """
    __slots__ = ('text',)
    
    def __new__(cls, *, text = ...):
        """
        Creates a new poll question with the given parameters.
        
        Parameters
        ----------
        text : `None`, `str`, Optional (Keyword only)
            The question's text.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # text
        if text is ...:
            text = None
        else:
            text = validate_text(text)
        
        # Construct
        self = object.__new__(cls)
        self.text = text
        return self
    
    
    def __len__(self):
        """Returns the poll question's length."""
        length = 0
        
        # text
        text = self.text
        if (text is not None):
            length += len(text)
        
        return length
    
    
    def __bool__(self):
        """Returns whether the poll question has any fields set."""
        # text
        if self.text is not None:
            return True
        
        return False
    
    
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # text
        text = self.text
        if (text is not None):
            repr_parts.append(' text = ')
            repr_parts.append(repr(text))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the poll question's hash value."""
        hash_value = 0
        
        # text
        text = self.text
        if (text is not None):
            hash_value ^= hash(text)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two poll questions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # text
        if self.text != other.text:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new poll question instance from the given json data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to create poll question from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.text = parse_text(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Returns the poll question as a json serializable representation.
        
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
        
        put_text(self.text, data, defaults)
        return data
    
    
    def clean_copy(self, guild = None):
        """
        Creates a clean copy of the poll question by removing the mentions in it's contents.
        
        Parameters
        ----------
        guild : ``None | Guild`` = `None`, Optional
            The respective guild as a context to look up guild specific names of entities.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.text = sanitize_mentions(self.text, guild)
        return new
    
    
    def copy(self):
        """
        Copies the poll question.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.text = self.text
        return new
    
    
    def copy_with(self, *, text = ...):
        """
        Copies the poll question with the given parameters.
        
        Parameters
        ----------
        text : `None`, `str`, Optional (Keyword only)
            The question's text.
        
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
        # text
        if text is ...:
            text = self.text
        else:
            text = validate_text(text)
        
        # Construct
        new = object.__new__(type(self))
        new.text = text
        return new
    
    
    @property
    def contents(self):
        """
        Returns the contents of the poll question.
        
        Returns
        -------
        contents : `list<str>`
        """
        return [*self.iter_contents()]
    
    
    def iter_contents(self):
        """
        Iterates over the contents of the poll question.
        
        This method is an iterable generator.
        
        Yields
        ------
        content : `str`
        """
        text = self.text
        if (text is not None):
            yield text
