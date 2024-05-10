__all__ = ('BanAddMultipleResult',)

from scarletio import RichAttributeErrorBaseType

from ...user import create_partial_user_from_id

from .fields import (
    parse_banned_user_ids, parse_failed_user_ids, put_banned_user_ids_into, put_failed_user_ids_into,
    validate_banned_user_ids, validate_failed_user_ids
)


class BanAddMultipleResult(RichAttributeErrorBaseType):
    """
    A ban add multiple result.
    
    Attributes
    ----------
    banned_user_ids : `None | tuple<int>`
        The actually banned users' identifiers.
    failed_user_ids : `None | tuple<int>`
        The failed to ban users' identifiers.
    """
    __slots__ = ('banned_user_ids', 'failed_user_ids',)
    
    def __new__(cls, *, banned_user_ids = ..., failed_user_ids = ...):
        """
        Creates a new ban add multiple result instance.
        
        Parameters
        ----------
        banned_user_ids : `None | iterable<int | ClientUserBase>`, Optional (Keyword only)
            The actually banned users' identifiers.
        failed_user_ids : `None | iterable<int | ClientUserBase>`, Optional (Keyword only)
            The failed to ban users' identifiers.
        
        Raises
        -------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # banned_user_ids
        if banned_user_ids is ...:
            banned_user_ids = None
        else:
            banned_user_ids = validate_banned_user_ids(banned_user_ids)
        
        # failed_user_ids
        if failed_user_ids is ...:
            failed_user_ids = None
        else:
            failed_user_ids = validate_failed_user_ids(failed_user_ids)
        
        # Construct
        self = object.__new__(cls)
        self.banned_user_ids = banned_user_ids
        self.failed_user_ids = failed_user_ids
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a ban add multiple result instance from the given `data`.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data representing a ban add multiple result.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.banned_user_ids = parse_banned_user_ids(data)
        self.failed_user_ids = parse_failed_user_ids(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the ban add multiple result into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_banned_user_ids_into(self.banned_user_ids, data, defaults)
        put_failed_user_ids_into(self.failed_user_ids, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the ban add multiple result's representation."""
        repr_parts = ['<', type(self).__name__]
        
        
        # banned_user_ids
        banned_user_ids = self.banned_user_ids
        if (banned_user_ids is not None):
            repr_parts.append(' banned_user_ids = ')
            repr_parts.append(repr(self.banned_user_ids))
            
            
            field_added = True
        else:
            field_added = False
        
        # failed_user_ids
        failed_user_ids = self.failed_user_ids
        if (failed_user_ids is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' failed_user_ids = ')
            repr_parts.append(repr(failed_user_ids))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __len__(self):
        """Helper for unpacking."""
        return 2
    
    
    def __iter__(self):
        """Unpacks the ban add multiple result."""
        yield self.banned_user_ids
        yield self.failed_user_ids

    
    def __hash__(self):
        """Returns the ban add multiple result's hash value."""
        hash_value = 0
        
        # banned_user_ids
        banned_user_ids = self.banned_user_ids
        if (banned_user_ids is not None):
            hash_value ^= len(banned_user_ids)
            for user_id in banned_user_ids:
                hash_value ^= user_id
        
        # failed_user_ids
        failed_user_ids = self.failed_user_ids
        if (failed_user_ids is not None):
            hash_value ^= len(failed_user_ids) << 8
            for user_id in failed_user_ids:
                hash_value ^= user_id
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two ban entries are equal."""
        if type(self) is not type(other):
            return False
        
        # reason
        if self.banned_user_ids != other.banned_user_ids:
            return False
        
        # user
        if self.failed_user_ids != other.failed_user_ids:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the ban add multiple result.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        banned_user_ids = self.banned_user_ids
        if (banned_user_ids is not None):
            banned_user_ids = (*banned_user_ids,)
        new.banned_user_ids = banned_user_ids
        
        failed_user_ids = self.failed_user_ids
        if (failed_user_ids is not None):
            failed_user_ids = (*failed_user_ids,)
        new.failed_user_ids = failed_user_ids
        
        return new
    
    
    def copy_with(self, *, banned_user_ids = ..., failed_user_ids = ...):
        """
        Copies the ban add multiple result.
        
        Parameters
        ----------
        banned_user_ids : `None | iterable<int | ClientUserBase>`, Optional (Keyword only)
            The actually banned users' identifiers.
        failed_user_ids : `None | iterable<int | ClientUserBase>`, Optional (Keyword only)
            The failed to ban users' identifiers.
        
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
        # banned_user_ids
        if banned_user_ids is ...:
            banned_user_ids = self.banned_user_ids
            if (banned_user_ids is not None):
                banned_user_ids = (*banned_user_ids,)
        else:
            banned_user_ids = validate_banned_user_ids(banned_user_ids)
        
        # failed_user_ids
        if failed_user_ids is ...:
            failed_user_ids = self.failed_user_ids
            if (failed_user_ids is not None):
                failed_user_ids = (*failed_user_ids,)
        else:
            failed_user_ids = validate_failed_user_ids(failed_user_ids)
        
        # Construct
        new = object.__new__(type(self))
        new.banned_user_ids = banned_user_ids
        new.failed_user_ids = failed_user_ids
        return new
    
    
    def iter_banned_user_ids(self):
        """
        Iterates over the banned users' identifiers.
        
        This method is an iterable generator.
        
        yields
        ------
        user_id : `int`
        """
        banned_user_ids = self.banned_user_ids
        if (banned_user_ids is not None):
            yield from banned_user_ids
    
    
    def iter_banned_users(self):
        """
        Iterates over the banned users.
        
        This method is an iterable generator.
        
        yields
        ------
        user : ``ClientUserBase`
        """
        banned_user_ids = self.banned_user_ids
        if (banned_user_ids is not None):
            for user_id in banned_user_ids:
                yield create_partial_user_from_id(user_id)
    
    
    def iter_failed_user_ids(self):
        """
        Iterates over the failed to ban users' identifiers.
        
        This method is an iterable generator.
        
        yields
        ------
        user_id : `int`
        """
        failed_user_ids = self.failed_user_ids
        if (failed_user_ids is not None):
            yield from failed_user_ids
    
    
    def iter_failed_users(self):
        """
        Iterates over the failed to ban users.
        
        This method is an iterable generator.
        
        yields
        ------
        user : ``ClientUserBase`
        """
        failed_user_ids = self.failed_user_ids
        if (failed_user_ids is not None):
            for user_id in failed_user_ids:
                yield create_partial_user_from_id(user_id)
