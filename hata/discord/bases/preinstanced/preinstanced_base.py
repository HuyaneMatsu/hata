__all__ = ('PreinstancedBase',)

from warnings import warn

from scarletio import RichAttributeErrorBaseType

from .preinstanced_meta import PreinstancedMeta


class PreinstancedBase(RichAttributeErrorBaseType, metaclass = PreinstancedMeta, base_type = True):
    """
    Base type for other preinstanced types.
    
    Attributes
    ----------
    name : `str`
        The name of the instance.
    
    value : `int | str`
        The value representing the instance.
    """
    __slots__ = ('name', 'value')
    
    
    def __new__(cls, value, name = None):
        """
        Creates a new preinstanced instance.
        
        Parameters
        ----------
        value : ``.VALUE_TYPE``
            The value of the preinstanced object.
        
        name : `None | str` = `None`, Optional
            The object's name.
        """
        if name is None:
            if cls.VALUE_TYPE is str:
                name = value
            else:
                name = cls.NAME_DEFAULT
        
        self = object.__new__(cls)
        self.value = value
        self.name = name
        return self
    
    
    @classmethod
    def get(cls, value):
        """
        Returns the value's representation. If the value is already preinstanced, returns that, else creates a new
        object.
        
        Parameters
        ----------
        value : `None`, ``.VALUE_TYPE``
            The value to get it's representation.
        
        Returns
        -------
        self : `type<cls>`
        """
        warn(
            (
                f'`{cls.__name__}` is deprecated and will be removed in 2025 September.'
                f'Please use `{cls.__name__}(value)` instead.',
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return cls(value)
    
    
    def __lt__(self, other):
        """Returns self < other."""
        self_type = type(self)
        other_type = type(other)
        
        if other_type is self_type:
            other_value = other.value
        elif other_type is self_type.VALUE_TYPE:
            other_value = other
        else:
            return NotImplemented
        
        return (self.value < other_value)
    
    
    def __gt__(self, other):
        """Returns self > other."""
        self_type = type(self)
        other_type = type(other)
        
        if other_type is self_type:
            other_value = other.value
        elif other_type is self_type.VALUE_TYPE:
            other_value = other
        else:
            return NotImplemented
        
        return (self.value > other_value)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if self is other:
            return True
        
        self_type = type(self)
        other_type = type(other)
        
        if other_type is self_type:
            other_value = other.value
        elif other_type is self_type.VALUE_TYPE:
            other_value = other
        else:
            return NotImplemented
        
        return (self.value == other_value)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        return hash(self.value)
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # value
        value = self.value
        repr_parts.append(' value = ')
        repr_parts.append(repr(value))
        
        # name | skip it, if same as value; some sub-types want to drop `.name` from `repr()` if its same as `.value`.
        name = self.name
        if (self.VALUE_TYPE is not str) or (value != name):
            repr_parts.append(', name = ')
            repr_parts.append(repr(self.name))
        
        # extra as available
        self._put_repr_parts_into(repr_parts)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _put_repr_parts_into(self, repr_parts):
        """
        Appends the representation parts.
        
        Parameters
        ----------
        repr_parts : `list<str>`
            Representation parts to extend.
        """
        return
