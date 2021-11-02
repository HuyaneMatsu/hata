# -*- coding: utf-8 -*-
__all__ = ('QualPath',)

class QualPath:
    """
    Represents a class's module path.
    
    Attributes
    ----------
    _hash : `None` or `int`
        Cached slot for the hash of the qual-path.
    _str : `None` or `str`
        Cached slot for `str` of the qual-path.
    parts : `list` of `str`
        Broken down parts of the module path.
    """
    __slots__ = ('_hash', '_str', 'parts',)
    
    def __new__(cls, *paths):
        """
        Creates a new ``QualPath`` object
        
        Parameters
        ----------
        *paths : `str` or ``QualPath`` instances
            Paths to create the qual-path from.
        
        Returns
        -------
        self : ``QualPath``
        
        Raises
        ------
        TypeError
            A path was given neither as `str` or as ``QualPath`` instance.
        ValueError
            A path was given as `str` instance, but it contains an empty sub-path.
        """
        parts = []
        for path in paths:
            if type(path) is cls:
                parts.extend(path.parts)
                continue
            
            if isinstance(path, str):
                if not path:
                    continue
                
                sub_parts = path.split('.')
                if len(sub_parts) == 1:
                    parts.append(sub_parts[0])
                    continue
                
                for sub_part in sub_parts:
                    if not sub_part:
                        raise ValueError(f'`{path!r}` contains empty sub-path.')
                parts.extend(sub_parts)
                continue
            
            raise TypeError(f'`path` passed neither as `str`, or `{cls.__name__} instance: {path.__class__.__name__}.')
        
        self = object.__new__(cls)
        self.parts = parts
        self._hash = None
        self._str = None
        return self
    
    def __str__(self):
        """Returns the qual-path's parts joined together."""
        str_ = self._str
        if str_ is None:
            self._str = str_ = '.'.join(self.parts)
        
        return str_
    
    def __repr__(self):
        """Returns the qual-path's representation."""
        result = [
            self.__class__.__name__,
            '(',
                ]
        
        parts = self.parts
        limit = len(parts)
        if limit:
            index = 0
            while True:
                part = parts[index]
                result.append(part)
                index +=1
                if index == limit:
                    break
                
                result.append(', ')
                continue
        
        result.append(')')
        
        return ''.join(result)
    
    def __truediv__(self, other):
        """Adds the two qual-path together returning a new one."""
        return type(self)(self, other)
    
    def __rtruediv__(self, other):
        """Adds the two qual-path together returning a new one."""
        return type(self)(other, self)
    
    def __eq__(self, other):
        """Returns whether the two values are the same."""
        if type(self) is type(other):
            return (self.parts == other.parts)
        
        if isinstance(other, str):
            return (str(self) == other)
        
        return NotImplemented
    
    def __sub__(self, other):
        """Subtracts from self's end the given other if applicable."""
        if type(other) is type(self):
            pass
        elif isinstance(other, str):
            other = type(self)(other)
        else:
            return NotImplemented
        
        return self._do_sub(other)
    
    def __rsub__(self, other):
        """Subtracts from the given other's end self if applicable."""
        if type(other) is type(self):
            pass
        elif isinstance(other, str):
            other = type(self)(other)
        else:
            return NotImplemented
        
        return other._do_sub(self)
    
    def _do_sub(self, other):
        """
        Subtracts other from self's end if applicable.
        
        This method is called by ``.__sub__`` and by ``.__rsub__``, after `other`'s type is validated to do the real
        work.
        
        Parameters
        ----------
        other : ``QualPath``
            The other qual-path to subtract.
        
        Returns
        -------
        new : ``QualPath``
        """
        self_parts = self.parts
        if not self_parts:
            return self
        
        other_parts = other.parts
        if not other_parts:
            return self
        
        other_to_find = other_parts[0]
        
        limit = len(self_parts)
        index = limit-len(other_parts)
        while True:
            if (self_parts[index] == other_to_find) and (self_parts[index:] == other_parts[:limit-index]):
                new = object.__new__(type(self))
                new.parts = self_parts[:index]
                new._hash = None
                new._str = None
                return new
            
            index += 1
            if index == limit:
                return self
    
    def __hash__(self):
        """Returns the path's hash."""
        hash_ = self._hash
        if hash_ is None:
            self._hash = hash_ = hash(str(self))
        
        return hash_
    
    def __contains__(self, value):
        """Returns whether self contains other."""
        if type(value) is type(self):
            value = str(value)
        elif isinstance(value, str):
            pass
        else:
            return False
        
        return (value in str(self))
    
    def __bool__(self):
        """Returns whether the path has any parts."""
        return (True if self.parts else False)
    
    @property
    def parent(self):
        """
        Does one step back on a new qual path object.
        
        Returns
        -------
        new : ``QualPath``
        """
        new = object.__new__(type(self))
        new.parts = self.parts[:-1]
        new._hash = None
        new._str = None
        return new
