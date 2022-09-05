__all__ = ('ActivitySecrets',)

from scarletio import copy_docs

from .base import ActivityFieldBase


def _assert__activity_secrets__join(join):
    """
    Asserts the `join` parameter of ``ActivitySecrets.__new__`` method.
    
    Parameters
    ----------
    join : `None`, `str`
        Unique hash given for the match context.
    
    Raises
    ------
    AssertionError
        - If `join` is not `None`, `str`.
    """
    if (join is not None) and (not isinstance(join, str)):
        raise AssertionError(
            f'`match` can be `None`, `str`, got {join.__class__.__name__}; {join!r}.'
        )
    
    return True


def _assert__activity_secrets__match(match):
    """
    Asserts the `match` parameter of ``ActivitySecrets.__new__`` method.
    
    Parameters
    ----------
    match : `None`, `str`
        Unique hash for spectate button.
    
    Raises
    ------
    AssertionError
        - If `match` is not `None`, `str`.
    """
    if (match is not None) and (not isinstance(match, str)):
        raise AssertionError(
            f'`match` can be `None`, `str`, got {match.__class__.__name__}; {match!r}.'
        )
    
    return True


def _assert__activity_secrets__spectate(spectate):
    """
    Asserts the `spectate` parameter of ``ActivitySecrets.__new__`` method.
    
    Parameters
    ----------
    spectate : `None`, `str`
        Unique hash for chat invites and ask to join.
    
    Raises
    ------
    AssertionError
        - If `spectate` is not `None`, `str`.
    """
    if (spectate is not None) and (not isinstance(spectate, str)):
        raise AssertionError(
            f'`spectate` can be `None`, `str`, got {spectate.__class__.__name__}; {spectate!r}.'
        )
    
    return True


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
    
    def __new__(cls, *, join=None, match=None, spectate=None):
        """
        Creates a new activity secret from the given parameters.
        
        Parameters
        ----------
        join : `None`, `str` = `None`, Optional (Keyword only)
            Unique hash given for the match context.
        match : `None`, `str` = `None`, Optional (Keyword only)
            Unique hash for spectate button.
        spectate : `None`, `str` = `None`, Optional (Keyword only)
            Unique hash for chat invites and ask to join.
        """
        assert _assert__activity_secrets__join(join)
        assert _assert__activity_secrets__match(match)
        assert _assert__activity_secrets__spectate(spectate)
        
        if (join is not None) and (not join):
            join = None
        
        if (match is not None) and (not match):
            match = None
        
        if (spectate is not None) and (not spectate):
            spectate = None
        
        self = object.__new__(cls)
        self.join = join
        self.match = match
        self.spectate = spectate
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, secrets_data):
        self = object.__new__(cls)
        self.join = secrets_data.get('join', None)
        self.spectate = secrets_data.get('spectate', None)
        self.match = secrets_data.get('match', None)
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self):
        secrets_data = {}
        
        join = self.join
        if (join is not None):
            secrets_data['join'] = join
        
        spectate = self.spectate
        if (spectate is not None):
            secrets_data['spectate'] = spectate
        
        match = self.match
        if (match is not None):
            secrets_data['match'] = match
        
        return secrets_data
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        join = self.join
        if (join is not None):
            repr_parts.append(' join=')
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
            repr_parts.append(' spectate=')
            repr_parts.append(repr(spectate))
        
        match = self.match
        if (match is not None):
            if field_added:
                repr_parts.append(',')
            repr_parts.append(' match=')
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
