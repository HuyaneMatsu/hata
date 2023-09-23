__all__ = ('GuildInventorySettings', )

from scarletio import RichAttributeErrorBaseType

from .fields import parse_emoji_pack_collectible, put_emoji_pack_collectible_into, validate_emoji_pack_collectible


class GuildInventorySettings(RichAttributeErrorBaseType):
    """
    A guild's inventory settings.
    
    Attributes
    ----------
    emoji_pack_collectible : `bool`
        Whether you can collect this guild's emojis and use it across all guilds.
    """
    __slots__ = ('emoji_pack_collectible', )
    
    def __new__(cls, *, emoji_pack_collectible = ...):
        """
        Creates a new guild inventory settings with the given fields.
        
        Parameters
        ----------
        emoji_pack_collectible : `bool`, Optional (Keyword only)
            Whether you can collect this guild's emojis and use it across all guilds.
        
        Raises
        ------
        TypeError
            - Parameter with incorrect type given.
        ValueError
            - Parameter with incorrect value given.
        """
        # emoji_pack_collectible
        if emoji_pack_collectible is ...:
            emoji_pack_collectible = False
        else:
            emoji_pack_collectible = validate_emoji_pack_collectible(emoji_pack_collectible)
        
        # Construct
        self = object.__new__(cls)
        self.emoji_pack_collectible = emoji_pack_collectible
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a guild inventory settings from the requested guild inventory settings data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received guild inventory settings data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.emoji_pack_collectible = parse_emoji_pack_collectible(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the guild inventory settings to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_emoji_pack_collectible_into(self.emoji_pack_collectible, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the guild inventory settings' representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        emoji_pack_collectible = self.emoji_pack_collectible
        if emoji_pack_collectible:
            repr_parts.append(' emoji_pack_collectible = ')
            repr_parts.append(repr(emoji_pack_collectible))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two guild inventory settings are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.emoji_pack_collectible != other.emoji_pack_collectible:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the guild inventory settings."""
        hash_value = 0
        
        # emoji_pack_collectible
        hash_value ^= self.emoji_pack_collectible
        
        return hash_value
    
    
    def __bool__(self):
        """Returns whether the guild has any features."""
        if self.emoji_pack_collectible:
            return True
        
        return False
    
    
    def copy(self):
        """
        Copies the guild inventory settings.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.emoji_pack_collectible = self.emoji_pack_collectible
        return new
    
    
    def copy_with(self, *, emoji_pack_collectible = ...):
        """
        Copies the guild inventory settings with the given fields.
        
        Parameters
        ----------
        emoji_pack_collectible : `bool`, Optional (Keyword only)
            Whether you can collect this guild's emojis and use it across all guilds.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - Parameter with incorrect type given.
        ValueError
            - Parameter with incorrect value given.
        """
        # emoji_pack_collectible
        if emoji_pack_collectible is ...:
            emoji_pack_collectible = self.emoji_pack_collectible
        else:
            emoji_pack_collectible = validate_emoji_pack_collectible(emoji_pack_collectible)
        
        # Construct
        new = object.__new__(type(self))
        new.emoji_pack_collectible = emoji_pack_collectible
        return new
