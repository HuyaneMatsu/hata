__all__ = ('GuildActivityOverviewTag',)

from scarletio import RichAttributeErrorBaseType

from .fields import parse_emoji, parse_title, put_emoji, put_title, validate_emoji, validate_title


class GuildActivityOverviewTag(RichAttributeErrorBaseType):
    """
    A tag of a guild activity overview.
    
    Attributes
    ----------
    emoji : ``None | Emoji``
        The tag's emoji.
    
    title : `str`
        The tag's emoji
    """
    __slots__ = ('emoji', 'title')
    
    def __new__(cls, *, emoji = ..., title = ...):
        """
        Creates a new guild activity overview tag.
        
        Parameters
        ----------
        emoji : ``None | Emoji``, Optional (Keyword only)
            The tag's emoji.
        
        title : `str`, Optional (Keyword only)
            The tag's emoji
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value in incorrect.
        """
        # emoji
        if emoji is ...:
            emoji = None
        else:
            emoji = validate_emoji(emoji)
        
        # title
        if title is ...:
            title = ''
        else:
            title = validate_title(title)
        
        # Construct
        self = object.__new__(cls)
        self.emoji = emoji
        self.title = title
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # emoji
        repr_parts.append(' emoji = ')
        repr_parts.append(repr(self.emoji))
        
        # title
        repr_parts.append(', title = ')
        repr_parts.append(repr(self.title))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= hash(emoji)
        
        # title
        hash_value ^= hash(self.title)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # emoji
        if self.emoji is not other.emoji:
            return False
        
        # title
        if self.title != other.title:
            return False
        
        return True
        
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new tag.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Channel data receive from Discord.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.emoji = parse_emoji(data)
        self.title = parse_title(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the guild activity overview tag.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_emoji(self.emoji, data, defaults)
        put_title(self.title, data, defaults)
        return data
    
    
    def copy(self):
        """
        Copies the guild activity overview tag.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.emoji = self.emoji
        new.title = self.title
        return new
    
    
    def copy_with(self, *, emoji = ..., title = ...):
        """
        Copies the guild activity overview tag with the given fields.
        
        Parameters
        ----------
        emoji : ``None | Emoji``, Optional (Keyword only)
            The tag's emoji.
        
        title : `str`, Optional (Keyword only)
            The tag's emoji
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value in incorrect.
        """
        # emoji
        if emoji is ...:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # title
        if title is ...:
            title = self.title
        else:
            title = validate_title(title)
        
        # Construct
        new = object.__new__(type(self))
        new.emoji = emoji
        new.title = title
        return new
