__all__ = ('GuildWidgetChannel',)

from ...bases import DiscordEntity

from .fields import (
    parse_id, parse_name, parse_position, put_id_into, put_name_into, put_position_into, validate_id, validate_name,
    validate_position
)


class GuildWidgetChannel(DiscordEntity):
    """
    Represents a ``GuildWidget``'s channel.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the guild widget channel.
    name : `str`
        The channel's name.
    position : `int`
        The channel's position.
    """
    __slots__ = ('name', 'position')
    
    
    def __new__(
        cls,
        *,
        channel_id = ...,
        name = ...,
        position = ...,
    ):
        """
        Creates a new guild widget channel with the given fields.
        
        Parameters
        ----------
        channel_id : `int`, Optional (Keyword only)
            The unique identifier number of the guild widget channel.
        name : `str`, Optional (Keyword only)
            The channel's name.
        position : `int`, Optional (Keyword only)
            The channel's position.
        
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
            channel_id = validate_id(channel_id)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # position
        if position is ...:
            position = 0
        else:
            position = validate_position(position)
        
        # Construct
        self = object.__new__(cls)
        self.id = channel_id
        self.name = name
        self.position = position
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new guild widget channel from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Guild widget channel data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = parse_id(data)
        self.name = parse_name(data)
        self.position = parse_position(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the guild widget channel.
        
        Parameters
        ----------
        defaults : `bool`
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_id_into(self.id, data, defaults)
        put_name_into(self.name, data, defaults)
        put_position_into(self.position, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the guild widget channel's representation."""
        return f'<{self.__class__.__name__} id = {self.id}, name = {self.name!r}>'
    
    
    def __hash__(self):
        """Returns the guild widget channel's hash value."""
        hash_value = 0
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        # position
        hash_value ^= hash(self.position)
        
        return hash_value
    
    
    def __gt__(self, other):
        """
        Whether this guild widget channel has greater (visible) position than the other at their respective guild.
        """
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_greater_than_same_type(other)
    
    
    def __ge__(self, other):
        """
        Whether this guild widget channel has greater or equal (visible) position than the other at their respective
        guild.
        """
        if type(self) is not type(other):
            return NotImplemented
    
        return self._is_greater_than_same_type(other) or self._is_equal_same_type(other)
    
    
    def __eq__(self, other):
        """Returns whether the two guild widget channels are equal."""
        if type(self) is not type(other):
            return NotImplemented
    
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two guild widget channels are not equal."""
        if type(self) is not type(other):
            return NotImplemented
    
        return not self._is_equal_same_type(other)
    
    
    def __le__(self, other):
        """
        Whether this guild widget channel has lower or equal (visible) position than the other at their respective
        guild.
        """
        if type(self) is not type(other):
            return NotImplemented
        
        return other._is_greater_than_same_type(self) or self._is_equal_same_type(other)
    
    
    def __lt__(self, other):
        """
        Whether this guild widget channel has lower (visible) position than the other at their respective guild.
        """
        if type(self) is not type(other):
            return NotImplemented
        
        return other._is_greater_than_same_type(self)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two guild widget channels are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `type(self)`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # id
        if self.id != other.id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # position
        if self.position != other.position:
            return False
        
        return True
    
    
    def _is_greater_than_same_type(self, other):
        """
        Returns whether self is greater than the other guild widget.
            
        Helper method for ``.__gt__`` and ``.__lt__`.
        
        Parameters
        ----------
        other : `type(self)`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_greater_than : `bool`
        """
        self_position = self.position
        other_position = other.position
        
        if self_position > other_position:
            return True
        
        if self_position < other_position:
            return False
        
        return self.id > other.id

    def copy(self):
        """
        Copies the guild widget channel.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.id = self.id
        new.name = self.name
        new.position = self.position
        return new
    
    
    def copy_with(
        self,
        *,
        name = ...,
        position = ...,
        channel_id = ...,
    ):
        """
        Copies the guild widget channel with the given fields.
        
        Parameters
        ----------
        channel_id : `int`, Optional (Keyword only)
            The unique identifier number of the guild widget channel.
        name : `str`, Optional (Keyword only)
            The channel's name.
        position : `int`, Optional (Keyword only)
            The channel's position.
        
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
            channel_id = self.id
        else:
            channel_id = validate_id(channel_id)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # position
        if position is ...:
            position = self.position
        else:
            position = validate_position(position)
        
        # Construct
        new = object.__new__(type(self))
        new.id = channel_id
        new.name = name
        new.position = position
        return new
    
    
    @property
    def mention(self):
        """
        The channel's mention.
        
        Returns
        -------
        mention : `str`
        """
        return f'<#{self.id}>'
