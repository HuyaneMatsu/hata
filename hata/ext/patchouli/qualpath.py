# -*- coding: utf-8 -*-
__all__ = ('QualPath',)

class QualPath(object):
    """
    Represents a classe's module path.
    
    Attributes
    ----------
    __hash : `None` or `int`
        Cached slot for the hash of the qualpath.
    parts : `list` of `str`
        Broken down parts of the module path.
    """
    __slots__ = ('__hash', 'parts', )
    
    def __new__(cls, *paths):
        """
        Creates a new ``QualPath`` object
        
        Parameters
        ----------
        *paths : `str` or ``QualPath`` instances
            Paths to create the qualpath from.
        
        Returns
        -------
        self : ``QualPath``
        
        Raises
        ------
        TypeError
            A path was given neither as `str` or as ``QualPath`` instance.
        ValueError
            A path was given as `str` instance, but it contains an empty subpath.
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
                        raise ValueError(f'`{path!r}` contains empty subpath.')
                parts.extend(sub_parts)
                continue
            
            raise TypeError(f'`path` passed neither as `str`, or `{cls.__name__} instance: {path.__class__.__name__}.')
        
        self = object.__new__(cls)
        self.parts = parts
        self.__hash = None
        return self
    
    def __str__(self):
        """Returns the qualpath's parts joined together."""
        return '.'.join(self.parts)
    
    def __repr__(self):
        """Returns the qualpath's represnetation."""
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
                index = index+1
                if index == limit:
                    break
                
                result.append(', ')
                continue
        
        result.append(')')
        
        return ''.join(result)
    
    def __truediv__(self, other):
        """Adds the two qualpath together returning a new one."""
        return type(self)(self, other)
    
    def __itruediv__(self, other):
        """Adds the two qualpaths together with extending self."""
        if type(other) is type(self):
            self.parts.extend(other.parts)
            self.__hash = None
            return
        
        if isinstance(other, str):
            if not other:
                return
            
            sub_parts = other.split('.')
            if len(sub_parts) == 1:
                self.parts.append(sub_parts[0])
                self.__hash = None
                return
            
            for sub_part in sub_parts:
                if not sub_part:
                    raise ValueError(f'`{other!r}` contains empty subpath.')
                
            self.parts.extend(sub_parts)
            self.__hash = None
            return
        
        raise TypeError(f'`path` passed neither as `str`, or `{self.__class__.__name__} instance: '
            f'{other.__class__.__name__}.')
    
    def __eq__(self, other):
        """Returns whether the two values are the same."""
        if type(self) is type(other):
            return (self.parts == other.parts)
        
        if isinstance(other, str):
            return (str(self) == other)
        
        return NotImplemented
    
    def __hash__(self):
        """Returns the path's hash."""
        hash_ = self.__hash
        if hash_ is None:
            self.__hash = hash_ = hash(str(self))
        
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
    
    def endswith(self, value):
        """
        Returns whether self ends with the given value.
        
        Parameters
        ----------
        value : `str`
        
        Returns
        -------
        endswith : `bool`
        """
        parts = self.parts
        if not parts:
            return False
        
        return (parts[-1] == value)
    
    def endswith_multy(self, values):
        """
        Returns whether self ends with the given inexable container.
        
        Parameters
        ----------
        values : `indexable-container` of `str`
        
        Returns
        -------
        endswith : `bool`
        """
        parts = self.parts
        values_length = len(values)
        if len(parts) < values_length:
            return False
        
        return (parts[-values_length:] == values)
    
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
        return new
