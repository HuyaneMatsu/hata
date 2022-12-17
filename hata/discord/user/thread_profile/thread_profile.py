__all__ = ('ThreadProfile',)

from scarletio import RichAttributeErrorBaseType

from ...utils import DISCORD_EPOCH_START

from .fields import (
    parse_flags, parse_joined_at, put_flags_into, put_joined_at_into, validate_flags, validate_joined_at
)
from .flags import ThreadProfileFlag



class ThreadProfile(RichAttributeErrorBaseType):
    """
    Represents an user's profile inside of a thread channel.
    
    Attributes
    ----------
    joined_at : `None`, `datetime`
        The date when the user joined the thread.
    flags : ``ThreadProfileFlag``
        user specific settings of the profile.
    """
    __slots__ = ('joined_at', 'flags',)
    
    
    def __new__(cls, *,  flags = ..., joined_at = ...):
        """
        Creates a new thread profile with the given parameters.
        
        Parameters
        ----------
        flags : ``ThreadProfileFlag``, `int`, Optional (Keyword only)
            user specific settings of the profile.
        joined_at : `None`, `datetime`, Optional (Keyword only)
            The date when the user joined the thread.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """
        # flags
        if flags is ...:
            flags = ThreadProfileFlag()
        else:
            flags = validate_flags(flags)
        
        # joined_at
        if joined_at is ...:
            joined_at = None
        else:
            joined_at = validate_joined_at(joined_at)
        
        self = object.__new__(cls)
        self.flags = flags
        self.joined_at = joined_at
        return self
    
    
    def __repr__(self):
        """Returns the thread profile's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __hash__(self):
        """Returns the thread profile's hash value."""
        hash_value = 0
        
        # flags
        hash_value ^= self.flags
        
        # joined_at
        joined_at = self.joined_at
        if (joined_at is not None):
            hash_value ^= hash(joined_at)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two thread profiles are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # flags
        if self.flags != other.flags:
            return False
        
        # joined_at
        if self.joined_at != other.joined_at:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a thread profile from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received thread profile data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.joined_at = parse_joined_at(data)
        self._update_attributes(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the thread profile to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        put_flags_into(self.flags, data, defaults)
        
        # joined_at
        if include_internals:
            put_joined_at_into(self.joined_at, data, defaults)
        
        return data
    
    
    def _update_attributes(self, data):
        """
        Updates the thread profile with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received thread profile data.
        """
        self.flags = parse_flags(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the thread profile and returns it's changed attributes in a `dict` within `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | flags             | ``ThreadProfileFlag``         |
        +-------------------+-------------------------------+
        """
        old_attributes = {}
        
        flags = parse_flags(data)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = flags
        
        return old_attributes
    
    
    def copy(self):
        """
        Copies the thread profile.
        
        Returns
        -------
        new : `instance<type<self>>
        """
        new = object.__new__(type(self))
        new.flags = self.flags
        new.joined_at = self.joined_at
        return new
    
    
    def copy_with(self, *, flags = ..., joined_at = ...):
        """
        Copies the thread profile and modifies the defined the defined fields of it.
        
        Parameters
        ----------
        flags : ``ThreadProfileFlag``, `int`, Optional (Keyword only)
            user specific settings of the profile.
        joined_at : `None`, `datetime`, Optional (Keyword only)
            The date when the user joined the thread.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """

        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
        # joined_at
        if joined_at is ...:
            joined_at = self.joined_at
        else:
            joined_at = validate_joined_at(joined_at)
        
        new = object.__new__(type(self))
        new.flags = flags
        new.joined_at = joined_at
        return new
    
    
    @property
    def created_at(self):
        """
        Returns ``.joined_at`` if set, else the Discord epoch.
        
        Returns
        -------
        created_at : `datetime`
        """
        created_at = self.joined_at
        if created_at is None:
            created_at = DISCORD_EPOCH_START
        
        return created_at
