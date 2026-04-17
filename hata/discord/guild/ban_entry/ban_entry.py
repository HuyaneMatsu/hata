__all__ = ('BanEntry',)

from scarletio import RichAttributeErrorBaseType

from .fields import parse_reason, parse_user, put_reason, put_user, validate_reason, validate_user


class BanEntry(RichAttributeErrorBaseType):
    """
    A ban entry.
    
    Attributes
    ----------
    user : ``ClientUserBase``
        The banned user.
    reason : `None`, `str`
        The ban reason if applicable.
    """
    __slots__ = ('reason', 'user',)
    
    def __new__(cls, user, reason):
        """
        Creates a new ban entry instance.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The banned user.
        reason : `None`, `str`
            The ban reason if applicable.
        
        Raises
        -------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        reason = validate_reason(reason)
        user = validate_user(user)
        
        # Construct
        self = object.__new__(cls)
        self.reason = reason
        self.user = user
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a ban entry instance from the given `data`.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data representing a ban entry.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.reason = parse_reason(data)
        self.user = parse_user(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the ban entry into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_reason(self.reason, data, defaults)
        put_user(self.user, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the ban entry's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # user
        repr_parts.append(' user = ')
        repr_parts.append(repr(self.user))
        
        # reason
        reason = self.reason
        if (reason is not None):
            repr_parts.append(' reason = ')
            repr_parts.append(repr(reason))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __len__(self):
        """Helper for unpacking."""
        return 2
    
    
    def __iter__(self):
        """Unpacks the ban entry."""
        yield self.user
        yield self.reason

    
    def __hash__(self):
        """Returns the ban entry's hash value."""
        hash_value = 0
        
        # reason
        reason = self.reason
        if (reason is not None):
            hash_value ^= hash(reason)
        
        # user
        hash_value ^= hash(self.user)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two ban entries are equal."""
        if type(self) is not type(other):
            return False
        
        # reason
        if self.reason != other.reason:
            return False
        
        # user
        if self.user != other.user:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the ban entry.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.reason = self.reason
        new.user = self.user
        return new
    
    
    def copy_with(self, *, reason = ..., user = ...):
        """
        Copies the ban entry.
        
        Parameters
        ----------
        reason : `None`, `str`, Optional (Keyword only)
            The ban reason if applicable.
        user : ``ClientUserBase``, Optional (Keyword only)
            The banned user.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        -------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # reason
        if reason is ...:
            reason = self.reason
        else:
            reason = validate_reason(reason)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        # Construct
        new = object.__new__(type(self))
        new.reason = reason
        new.user = user
        return new
