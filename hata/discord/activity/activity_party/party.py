__all__ = ('ActivityParty',)

import warnings

from scarletio import copy_docs

from ..activity_field_base import ActivityFieldBase

from .fields import (
    parse_id, parse_size_and_max, put_id_into, put_size_and_max_into, validate_id, validate_max, validate_size
)


class ActivityParty(ActivityFieldBase):
    """
    Represents a discord activity party.
    
    Attributes
    ----------
    id : `None`, `str`
        The party's id, which in the player is.
    size : `int`
        The party's maximal size in which the player is. Defaults to `0`.
    max : `int`
        The party's actual size in which the player is. Defaults to `0`.
    """
    __slots__ = ('id', 'size', 'max',)
    
    def __new__(cls, *, party_id = ..., id_ = ..., size = ..., max_ = ...):
        """
        Creates a new activity party instance form the given parameters.
        
        Parameters
        ----------
        party_id : `None`, `str`, Optional (Keyword only)
            The party's id, which in the player is.
        size : `int`, Optional (Keyword only)
            The party's maximal size, which in the player is.
        max_ : `int`, Optional (Keyword only)
            The party's actual size, which in the player is.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        if id_ is not ...:
            warnings.warn(
                (
                    f'`{cls.__name__}.__new__`\'s `type_` parameter is deprecated and will be removed in 2023 Marc. '
                    f'Please use `activity_type` instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            party_id = id_
        
        # party_id
        if party_id is ...:
            party_id = None
        else:
            party_id = validate_id(party_id)
        
        # size
        if size is ...:
            size = 0
        else:
            size = validate_size(size)
        
        # max_
        if max_ is ...:
            max_ = 0
        else:
            max_ = validate_max(max_)
        
        # Construct
        self = object.__new__(cls)
        self.id = party_id
        self.size = size
        self.max = max_
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.id = parse_id(data)
        self.size, self.max = parse_size_and_max(data)
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_id_into(self.id, data, defaults)
        put_size_and_max_into((self.size, self.max), data, defaults)
        return data
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        party_id = self.id
        if (party_id is not None):
            repr_parts.append(' id = ')
            repr_parts.append(repr(party_id))
            field_added = True
        else:
            field_added = False
        
        size = self.size
        max_ = self.max
        if size or max_:
            if field_added:
                repr_parts.append(',')
            repr_parts.append(' size = ')
            repr_parts.append(repr(size))
            repr_parts.append(', max = ')
            repr_parts.append(repr(max_))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ActivityFieldBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.id != other.id:
            return False
        
        if self.size != other.size:
            return False
        
        if self.max != other.max:
            return False
        
        return True
    

    @copy_docs(ActivityFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        party_id = self.id
        if (party_id is not None):
            hash_value ^= hash(party_id)
            hash_value ^= (1 << 0)
        
        size = self.size
        if size:
            hash_value ^= size << 4
            hash_value ^= (1 << 1)
        
        max_ = self.max
        if max_:
            hash_value ^= max_ << 8
            hash_value ^= (1 << 2)
        
        return hash_value
    
    
    @copy_docs(ActivityFieldBase.__bool__)
    def __bool__(self):
        if (self.id is not None):
            return True
        
        size = self.size
        if size:
            return True
        
        max_ = self.max
        if max_:
            return True
        
        return False
    
    
    @copy_docs(ActivityFieldBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.id = self.id
        new.size = self.size
        new.max = self.max
        return new
    
    
    def copy_with(self, party_id = ..., id_ = ..., size = ..., max_ = ...):
        """
        Copies the activity party with the given fields.
        
        Parameters
        ----------
        party_id : `None`, `str`, Optional (Keyword only)
            The party's id, which in the player is.
        size : `int`, Optional (Keyword only)
            The party's maximal size, which in the player is.
        max_ : `int`, Optional (Keyword only)
            The party's actual size, which in the player is.
        
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

        # party_id
        if party_id is ...:
            party_id = self.id
        else:
            party_id = validate_id(party_id)
        
        # size
        if size is ...:
            size = self.size
        else:
            size = validate_size(size)
        
        # max_
        if max_ is ...:
            max_ = self.max
        else:
            max_ = validate_max(max_)
        
        # Construct
        new = object.__new__(type(self))
        new.id = party_id
        new.size = size
        new.max = max_
        return new
