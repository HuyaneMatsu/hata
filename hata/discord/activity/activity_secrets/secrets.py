__all__ = ('ActivitySecrets',)

from scarletio import copy_docs

from ..activity_field_base import ActivityFieldBase

from .fields import (
    parse_join, parse_match, parse_spectate, put_join_into, put_match_into, put_spectate_into, validate_join,
    validate_match, validate_spectate
)


class ActivitySecrets(ActivityFieldBase):
    """
    Represents and activity secret.
    
    Attributes
    ----------
    join : `None`, `str`
        Unique hash given for the match context.
    match : `None`, `str`
        Unique hash for spectate button.
    spectate : `None`, `str`
        Unique hash for chat invites and ask to join.
    """
    __slots__ = ('join', 'match', 'spectate', )
    
    def __new__(cls, *, join = ..., match = ..., spectate = ...):
        """
        Creates a new activity secret from the given parameters.
        
        Parameters
        ----------
        join : `None`, `str`, Optional (Keyword only)
            Unique hash given for the match context.
        match : `None`, `str`, Optional (Keyword only)
            Unique hash for spectate button.
        spectate : `None`, `str`, Optional (Keyword only)
            Unique hash for chat invites and ask to join.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # join
        if join is ...:
            join = None
        else:
            join = validate_join(join)
        
        # match
        if match is ...:
            match = None
        else:
            match = validate_match(match)
        
        # spectate
        if spectate is ...:
            spectate = None
        else:
            spectate = validate_spectate(spectate)
        
        # Construct
        self = object.__new__(cls)
        self.join = join
        self.match = match
        self.spectate = spectate
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.join = parse_join(data)
        self.match = parse_match(data)
        self.spectate = parse_spectate(data)
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_join_into(self.join, data, defaults)
        put_match_into(self.match, data, defaults)
        put_spectate_into(self.spectate, data, defaults)
        return data
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        join = self.join
        if (join is not None):
            repr_parts.append(' join = ')
            repr_parts.append(repr(join))
            field_added = True
        else:
            field_added = False
        
        spectate = self.spectate
        if (spectate is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' spectate = ')
            repr_parts.append(repr(spectate))
        
        match = self.match
        if (match is not None):
            if field_added:
                repr_parts.append(',')
            repr_parts.append(' match = ')
            repr_parts.append(repr(match))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ActivityFieldBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.join != other.join:
            return False
        
        if self.spectate != other.spectate:
            return False
        
        if self.match != other.match:
            return False
        
        return True
    

    @copy_docs(ActivityFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        join = self.join
        if (join is not None):
            hash_value ^= hash(join)
            hash_value ^= (1 << 0)
        
        spectate = self.spectate
        if (spectate is not None):
            hash_value ^= hash(spectate)
            hash_value ^= (1 << 4)
        
        match = self.match
        if (match is not None):
            hash_value ^= hash(match)
            hash_value ^= (1 << 8)
        
        return hash_value
    
    
    @copy_docs(ActivityFieldBase.__bool__)
    def __bool__(self):
        join = self.join
        if (join is not None):
            return True
        
        spectate = self.spectate
        if (spectate is not None):
            return True
        
        match = self.match
        if (match is not None):
            return True
        
        return False
    
    
    @copy_docs(ActivityFieldBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.join = self.join
        new.spectate = self.spectate
        new.match = self.match
        return new
    
    
    def copy_with(self, *, join = ..., match = ..., spectate = ...):
        """
        Copies the activity secrets with the given fields.
        
        Parameters
        ----------
        join : `None`, `str`, Optional (Keyword only)
            Unique hash given for the match context.
        match : `None`, `str`, Optional (Keyword only)
            Unique hash for spectate button.
        spectate : `None`, `str`, Optional (Keyword only)
            Unique hash for chat invites and ask to join.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # join
        if join is ...:
            join = self.join
        else:
            join = validate_join(join)
        
        # match
        if match is ...:
            match = self.match
        else:
            match = validate_match(match)
        
        # spectate
        if spectate is ...:
            spectate = self.spectate
        else:
            spectate = validate_spectate(spectate)
        
        # Construct
        new = object.__new__(type(self))
        new.join = join
        new.match = match
        new.spectate = spectate
        return new
