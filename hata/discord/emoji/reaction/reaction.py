__all__ = ('Reaction',)

from scarletio import RichAttributeErrorBaseType

from ..emoji import Emoji

from .fields import parse_emoji, parse_type, put_emoji, put_type, validate_emoji, validate_type
from .preinstanced import ReactionType


class Reaction(RichAttributeErrorBaseType):
    """
    Represents a reaction.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The reaction emoji,
    reaction_type : ``ReactionType``
        The reaction's type
    """
    __slots__ = ('emoji', 'type')
    
    def __new__(cls, emoji, *, reaction_type = ...):
        """
        Creates a new new reaction with the given parameters.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The reaction emoji,
        reaction_type : ``ReactionType``, `int`, Optional (Keyword only)
            The reaction's type.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # emoji
        emoji = validate_emoji(emoji)
        
        # reaction_type
        if reaction_type is ...:
            reaction_type = ReactionType.standard
        else:
            reaction_type = validate_type(reaction_type)
        
        # Construct
        self = object.__new__(cls)
        self.emoji = emoji
        self.type = reaction_type
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new reaction.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Reaction data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        emoji = parse_emoji(data)
        reaction_type = parse_type(data)
        
        self = object.__new__(cls)
        self.emoji = emoji
        self.type = reaction_type
        return self
    
    
    @classmethod
    def from_fields(cls, emoji, reaction_type):
        """
        Creates a new reaction from the given fields. Not like ``.__new__``, this has no validation.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The reaction emoji,
        reaction_type : ``ReactionType``
            The reaction's type
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.emoji = emoji
        self.type = reaction_type
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the reaction field.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_emoji(self.emoji, data, defaults)
        put_type(self.type, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the reaction's representation."""
        repr_parts = ['<',self.__class__.__name__]
        
        repr_parts.append(' emoji = ')
        repr_parts.append(repr(self.emoji))
        
        reaction_type = self.type
        repr_parts.append(', type = ')
        repr_parts.append(reaction_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(reaction_type.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two reaction's are equal."""
        other_type = type(other)
        if other_type is type(self):
            if self.emoji is not other.emoji:
                return False
            
            if self.type is not other.type:
                return False
            
            return True
        
        if other_type is Emoji:
            if self.emoji is not other:
                return False
            
            # If the other entity is an Emoji, only match it if we are standard
            if self.type is not ReactionType.standard:
                return False
            
            return True
        
        return NotImplemented
    
    
    def __hash__(self):
        """returns the reaction's hash value."""
        hash_value = 0
        
        # emoji
        hash_value ^= hash(self.emoji)
        
        # reaction_type
        hash_value ^= hash(self.type)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the reaction returning a new one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.emoji = self.emoji
        new.type = self.type
        return new
    
    
    def copy_with(self, *, emoji = ..., reaction_type = ...):
        """
        Copies the reaction with the given fields.
        
        Parameters
        ----------
        emoji : ``Emoji``, Optional (Keyword only)
            The reaction emoji,
        reaction_type : ``ReactionType``, Optional (Keyword only)
            The reaction's type.
        
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
        
        # type
        if reaction_type is ...:
            reaction_type = self.type
        else:
            reaction_type = validate_type(reaction_type)
        
        # Construct
        new = object.__new__(type(self))
        new.emoji = emoji
        new.type = reaction_type
        return new
