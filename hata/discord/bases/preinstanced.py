__all__ = ('Preinstance', 'PreinstancedBase', )

from scarletio import RichAttributeErrorBaseType


class Preinstance:
    """
    name : `str`
        The instance's name.
    value : `str`, `int`
        The instance's value.
    args : `tuple` of `Any`
        Additional parameters to preinstance with.
    """
    __slots__ = ('name', 'value', 'args')
    
    def __new__(cls, value, name, *args):
        """
        Creates a new ``Preinstance`` with the given parameters.
        
        Parameters
        ----------
        value : `str`, `int`
            The instance's value.
        name : `str`
            The instance's name.
        *args : Parameters
            Additional parameters to preinstance with.
        """
        self = object.__new__(cls)
        self.name = name
        self.value = value
        self.args = args
        return self
    
    def __repr__(self):
        """Returns the preinstanced's representation."""
        repr_parts = [
            self.__class__.__name__, '(',
            repr(self.value), ', ', repr(self.name),
        ]
        
        args = self.args
        for arg in args:
            repr_parts.append(', ')
            repr_parts.append(repr(arg))
        
        repr_parts.append(')')
        
        return ''.join(repr_parts)


class PreinstancedMeta(type):
    """
    Metaclass for ``PreinstancedBase``.
    """
    def __new__(cls, class_name, class_parents, class_attributes):
        """
        Creates a preinstanced type.
        
        Parameters
        ----------
        class_name : `str`
            The created class's name.
        class_parents : `tuple` of `type`
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `Any`) items
            The class attributes of the created type.
        
        Returns
        -------
        type : ``PreinstancedMeta``
        """
        post_instance = []
        new_class_attributes = {}
        for attribute_name, attribute_value in class_attributes.items():
            if isinstance(attribute_value, Preinstance):
                post_instance.append((attribute_name, attribute_value))
            else:
                new_class_attributes[attribute_name] = attribute_value
        
        type_ = type.__new__(cls, class_name, class_parents, new_class_attributes)
        
        for attribute_name, attribute_value in post_instance:
            setattr(type_, attribute_name, type_(attribute_value.value, attribute_value.name, *attribute_value.args)),
        
        return type_


class PreinstancedBase(RichAttributeErrorBaseType, metaclass = PreinstancedMeta):
    """
    Base class for preinstanced types.
    
    Class Attributes
    ----------------
    INSTANCES : `NoneType` = `NotImplemented`
        The instances of the preinstanced type. Subclasses should overwrite it as `dict`.
    VALUE_TYPE : `type` = `NoneType`
        The preinstanced object's value's type. Subclasses should overwrite it.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name to use as the preinstanced objects'.
    """
    INSTANCES = NotImplemented
    VALUE_TYPE = type(None)
    DEFAULT_NAME = 'Undefined'
    
    __slots__ = ('name', 'value',)
    
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
        obj_ : ``PreinstancedBase``
        """
        if value is None:
            value_type = cls.VALUE_TYPE
            if value_type is int:
                value = 0
            
            elif value_type is str:
                value = ''
            
            else:
                raise NotImplementedError(
                    f'Getting `{cls.__name__}` with value of `None` failed.'
                )
        
        try:
            obj_ = cls.INSTANCES[value]
        except KeyError:
            obj_ = cls._from_value(value)
        
        return obj_
    
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new preinstanced object from the given value.
        
        Parameters
        ----------
        value : ``.VALUE_TYPE``
            The value what has no representation yet.
        
        Returns
        -------
        self : ``PreinstancedBase``
            The created object.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = cls.DEFAULT_NAME
        self.INSTANCES[value] = self
        return self
    
    
    def __init__(self, value, name):
        """
        Creates a new preinstanced instance.
        
        Parameters
        ----------
        value : ``.VALUE_TYPE``
            The value of the preinstanced object.
        name : `str`
            The object's name.
        """
        self.value = value
        self.name = name
        self.INSTANCES[value] = self
    
    
    def __gt__(self, other):
        """Returns whether self's value is greater than the other object's."""
        other_type = other.__class__
        self_type = self.__class__
        if other_type is self_type:
            other_value = other.value
        elif other_type is self_type.VALUE_TYPE:
            other_value = other
        else:
            return NotImplemented
        
        if self.value > other_value:
            return True
        else:
            return False
    
    
    def __ge__(self, other):
        """Returns whether self's value is greater or equal to the other object's."""
        if self is other:
            return True
        
        other_type = other.__class__
        self_type = self.__class__
        if other_type is self_type:
            other_value = other.value
        elif other_type is self_type.VALUE_TYPE:
            other_value = other
        else:
            return NotImplemented
        
        if self.value >= other_value:
            return True
        else:
            return False
    
    
    def __eq__(self, other):
        """Returns whether self's value equals to the other object's."""
        if self is other:
            return True
        
        other_type = other.__class__
        self_type = self.__class__
        if other_type is self_type:
            other_value = other.value
        elif other_type is self_type.VALUE_TYPE:
            other_value = other
        else:
            return NotImplemented
        
        if self.value == other_value:
            return True
        else:
            return False
    
    
    def __ne__(self, other):
        """Returns whether self's not equals to the other object's."""
        if self is other:
            return False
        
        other_type = other.__class__
        self_type = self.__class__
        if other_type is self_type:
            other_value = other.value
        elif other_type is self_type.VALUE_TYPE:
            other_value = other
        else:
            return NotImplemented
        
        if self.value != other_value:
            return True
        else:
            return False
    
    
    def __le__(self, other):
        """Returns whether self's value is less or equal to the other object's."""
        if self is other:
            return True
        
        other_type = other.__class__
        self_type = self.__class__
        if other_type is self_type:
            other_value = other.value
        elif other_type is self_type.VALUE_TYPE:
            other_value = other
        else:
            return NotImplemented
        
        if self.value <= other_value:
            return True
        else:
            return False
    
    
    def __lt__(self, other):
        """Returns whether self's value is less than the other object's."""
        other_type = other.__class__
        self_type = self.__class__
        if other_type is self_type:
            other_value = other.value
        elif other_type is self_type.VALUE_TYPE:
            other_value = other
        else:
            return NotImplemented
        
        if self.value < other_value:
            return True
        else:
            return False
    
    
    def __hash__(self):
        """Returns the hash of the preinstanced object."""
        return hash(self.value)
    
    
    def __repr__(self):
        """Returns the representation of the preinstanced object."""
        return f'<{self.__class__.__name__} value = {self.value!r}, name = {self.name!r}>'
