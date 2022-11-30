__all__ = ('ActivityParty', )

import warnings

from scarletio import copy_docs

from .base import ActivityFieldBase


def _assert__activity_secrets__id(id_):
    """
    Asserts the `id_` parameter of ``ActivitySecrets.__new__`` method.
    
    Parameters
    ----------
    id_ : `None`, `str`
        The party's id, which in the player is.
    
    Raises
    ------
    AssertionError
        - If `id_` is not `None`, `str`.
    """
    if (id_ is not None) and (not isinstance(id_, str)):
        raise AssertionError(
            f'`id_` can be `None`, `str`, got {id_.__class__.__name__}; {id_!r}.'
        )
    
    return True


def _assert__activity_secrets__size(size):
    """
    Asserts the `size` parameter of ``ActivitySecrets.__new__`` method.
    
    Parameters
    ----------
    size : `int`
        The party's maximal size in which the player is.
    
    Raises
    ------
    AssertionError
        - If `size` is not `int`.
        - If `size` is negative`.
    """
    if (not isinstance(size, int)):
        raise AssertionError(
            f'`size` can be `int`, got {size.__class__.__name__}; {size!r}.'
        )
    
    if (size < 0):
        raise AssertionError(
            f'`size` cannot be negative, got {size!r}.'
        )
    
    return True


def _assert__activity_secrets__max(max_):
    """
    Asserts the `max_` parameter of ``ActivitySecrets.__new__`` method.
    
    Parameters
    ----------
    max_ : `int`
        The party's actual size in which the player is.
    
    Raises
    ------
    AssertionError
        - If `max_` is not `int`.
        - If `max_` is negative`.
    """
    if (not isinstance(max_, int)):
        raise AssertionError(
            f'`max_` can be `int`, got {max_.__class__.__name__}; {max_!r}.'
        )
    
    if (max_ < 0):
        raise AssertionError(
            f'`max_` cannot be negative, got {max_!r}.'
        )
    
    return True


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
    
    def __new__(cls, *, party_id = None, id_ = ..., size = 0, max_ = 0):
        """
        Creates a new activity party instance form the given parameters.
        
        Parameters
        ----------
        id_ : `None` = `None`, `str`, Optional (Keyword only)
            The party's id, which in the player is.
        size : `int` = `0`, Optional (Keyword only)
            The party's maximal size, which in the player is.
        max_ : `int` = `0`, Optional (Keyword only)
            The party's actual size, which in the player is.
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
        
        assert _assert__activity_secrets__id(party_id)
        assert _assert__activity_secrets__size(size)
        assert _assert__activity_secrets__max(max_)
        
        if (party_id is not None) and (not party_id):
            party_id = None
        
        self = object.__new__(cls)
        self.id = party_id
        self.size = size
        self.max = max_
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, party_data):
        self = object.__new__(cls)
        self.id = party_data.get('id', None)
        
        try:
            size, max_ = party_data['size']
        except KeyError:
            size = 0
            max_ = 0
        
        self.size = size
        self.max = max_
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self):
        party_data = {}
        
        id_ = self.id
        if (id_ is not None):
            party_data['id'] = id_
        
        size = self.size
        max_ = self.max
        if size or max_:
            party_data['size'] = [size, max_]
        
        return party_data
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        id_ = self.id
        if (id_ is not None):
            repr_parts.append(' id_=')
            repr_parts.append(repr(id_))
            field_added = True
        else:
            field_added = False
        
        size = self.size
        max_ = self.max
        if size or max_:
            if field_added:
                repr_parts.append(',')
            repr_parts.append(' size=')
            repr_parts.append(repr(size))
            repr_parts.append(', max=')
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
        
        id_ = self.id
        if (id_ is not None):
            hash_value ^= hash(id_)
            hash_value ^= (1 << 0)
        
        size = self.size
        if size:
            hash_value ^= hash(size)
            hash_value ^= (1 << 4)
        
        max_ = self.max
        if max_:
            hash_value ^= hash(max_)
            hash_value ^= (1 << 8)
        
        return hash_value
    
    
    @copy_docs(ActivityFieldBase.__bool__)
    def __bool__(self):
        id_ = self.id
        if (id_ is not None):
            return True
        
        size = self.size
        if size:
            return True
        
        max_ = self.max
        if max_:
            return True
        
        return False
