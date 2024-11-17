__all__ = ('FlagBase', 'FlagBaseReversed')

from warnings import warn

from scarletio import class_property, copy_docs

from .flag_meta import FlagMeta


class FlagBase(int, metaclass = FlagMeta):
    """
    Base type for bitwise flags.
    """
    def __repr__(self):
        """Returns the representation of the flag."""
        return f'{type(self).__name__}({self:d})'
    
    
    @classmethod
    def _get_shift_of(cls, key):
        """
        Gets the shift value for the given keys.
        
        Parameters
        ----------
        keys : `str`
            The key's name.
        
        Returns
        -------
        shift : `int`
        
        Raises
        ------
        LookupError
            - Invalid key given.
        """
        try:
            shift = cls.__shifts__[key]
        except KeyError:
            pass
        
        else:
            return shift
        
        try:
            shift, deprecation = cls.__deprecated_shifts__[key]
        except KeyError:
            pass
        else:
            deprecation.trigger(cls.__name__, key, 4)
            return shift
        
        # support `_(\d+)` format
        if key.startswith('_'):
            try:
                shift = int(key[1:])
            except ValueError:
                pass
            else:
                return shift
        
        raise LookupError(f'Invalid key: {key!r}.')
    
    
    def __getitem__(self, key):
        """
        Returns whether the specific flag of the given name is enabled.
        
        Parameters
        ----------
        
        Returns
        -------
        contains : `bool`
        """
        shift = self._get_shift_of(key)
        return True if (self >> shift) & 1 else False
    
    
    __contains__ = __getitem__
    
    
    def keys(self):
        """
        Yields the name of the bitwise flags, which are enabled.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
        """
        for name, shift in self.__shifts_ordered__:
            if (self >> shift) & 1:
                yield name
    
    
    __iter__ = keys
    
    
    def values(self):
        """
        Yields the shift values of the flags, under which shift value the flag is enabled.
        
        This method is an iterable generator.
        
        Yields
        -------
        shift : `int`
        """
        for name, shift in self.__shifts_ordered__:
            if (self >> shift) & 1:
                yield shift
    
    
    def items(self):
        """
        Yields the items of the flag.
        
        This method is an iterable generator.
        
        Yields
        ------
        item : `(str, bool)`
            Flag-name, enabled items.
        """
        for name, shift in self.__shifts_ordered__:
            yield name, True if (self >> shift) & 1 else False
    
    
    def is_subset(self, other):
        """Returns whether self has the same amount or more flags disabled than other."""
        return (self & other) == self
    
    
    def is_superset(self, other):
        """Returns whether self has the same amount or more flags enabled than other."""
        return (self | other) == self
    
    
    def is_strict_subset(self, other):
        """Returns whether self has more flags disabled than other."""
        return self != other and (self & other) == self
    
    
    def is_strict_superset(self, other):
        """Returns whether self has more flags enabled than other."""
        return self != other and (self | other) == self
    
    
    def update_by_keys(self, **keyword_parameters):
        """
        Updates the source value with the given flags and returns a new one.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            `flag-name` - `bool` relations.
        
        Returns
        -------
        flag : `instance<type<self>>`
        
        Raises
        ------
        LookupError
            If a keyword is invalid.
        
        Examples
        -------
        ```py
        >>> from hata import Permission
        >>> perm = Permission().update_by_keys(kick_users = True, ban_users = True)
        >>> list(perm)
        ['kick_users', 'ban_users']
        >>> perm = perm.update_by_keys(manage_roles = True, kick_users = False)
        >>> list(perm)
        ['ban_users', 'manage_roles']
        ```
        """
        new = self
        for key, value in keyword_parameters.items():
            shift = self._get_shift_of(key)
            
            if value:
                new |= (1 << shift)
            else:
                if (new >> shift) & 1:
                    new ^= (1 << shift)
        
        return int.__new__(type(self), new)

    
    @class_property
    def __keys__(cls):
        """
        Deprecated and will be removed in 2025 April. Please use `.__shifts__` instead.
        """
        warn(
            'Deprecated and will be removed in 2025 April. Please use `.__shifts__` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        return cls.__shifts__


class FlagBaseReversed(FlagBase, reverse_descriptors = True):
    """
    Base class for reversed bitwise flags.
    """
    @copy_docs(FlagBase.__getitem__)
    def __getitem__(self, key):
        shift = self._get_shift_of(key)
        return False if (self >> shift) & 1 else True
    
    
    __contains__ = __getitem__
    
    
    @copy_docs(FlagBase.keys)
    def keys(self):
        for name, shift in self.__shifts_ordered__:
            if ((self >> shift) & 1) ^ 1:
                yield name
    
    __iter__ = keys
    
    
    @copy_docs(FlagBase.values)
    def values(self):
        for name, shift in self.__shifts_ordered__:
            if not (self >> shift) & 1:
                yield shift
    
    
    @copy_docs(FlagBase.items)
    def items(self):
        for name, shift in self.__shifts_ordered__:
            yield name, False if ((self >> shift) & 1) else True
    
    
    @copy_docs(FlagBase.is_subset)
    def is_subset(self, other):
        return (self | other) == self
    
    
    @copy_docs(FlagBase.is_superset)
    def is_superset(self, other):
        return (self & other) == self
    
    
    @copy_docs(FlagBase.is_strict_subset)
    def is_strict_subset(self, other):
        return self != other and (self | other) == self
    
    
    @copy_docs(FlagBase.is_strict_superset)
    def is_strict_superset(self, other):
        return self != other and (self & other) == self
    
    
    @copy_docs(FlagBase.update_by_keys)
    def update_by_keys(self, **keyword_parameters):
        new = self
        for key, value in keyword_parameters.items():
            shift = self._get_shift_of(key)
            
            if value:
                if (new >> shift) & 1:
                    new ^= (1 << shift)
            else:
                new |= (1 << shift)
        
        return int.__new__(type(self), new)
