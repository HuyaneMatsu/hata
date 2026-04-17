__all__ = ()

from scarletio import RichAttributeErrorBaseType, docs_property


class PlaceHolderBase(RichAttributeErrorBaseType):
    __type_doc__ = (
    """
    Base type of place holders.
    
    Attributes
    ----------
    attribute_name : `None | str`
        The name of the place held attribute.
    
    docs : `None | str`
        Documentation of the place held attribute.
    
    type_name : `None | str`
        The name of the type the we place held at.
    """)
    
    @property
    def __instance_doc__(self):
        return self.docs
    
    __doc__ = docs_property()
    
    __slots__ = ('attribute_name', 'docs', 'type_name')

    def __new__(cls, docs = None):
        """
        Creates a new slot place holder.
        
        Parameters
        ----------
        docs : `None`, `str` = `None`, Optional
            Documentation of the place held attribute.
        """
        self = object.__new__(cls)
        self.attribute_name = None
        self.docs = docs
        self.type_name = None
        return self
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Helper function for ``.__eq__``. Returns whether the two instances are equal.
        Other must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance to compare self to.
        
        Returns
        -------
        is_equal : `bool`
        """
        # type_name
        if self.type_name != other.type_name:
            return False
        
        # docs
        if self.docs != other.docs:
            return False
        
        # attribute_name
        if self.attribute_name != other.attribute_name:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        type_name = self.type_name
        attribute_name = self.attribute_name
        if (type_name is None) or (attribute_name is None):
            field_added = False
        
        else:
            repr_parts.append(' of ')
            repr_parts.append(type_name)
            repr_parts.append('.')
            repr_parts.append(attribute_name)
            
            field_added = True
        
        field_added = self._put_repr_parts_into(repr_parts, field_added)
        
        docs = self.docs
        if (docs is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' docs = ')
            repr_parts.append(repr(docs))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _put_repr_parts_into(self, repr_parts, field_added):
        """
        Helper function for sub-types to extend the created representation.
        
        Parameters
        ----------
        repr_parts : `list<str>`
            Representation parts to extended.
        
        field_added : `bool`
            Whether a field was already added to representation.
        
        Returns
        -------
        field_added : `bool`
        """
        return field_added
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # docs
        docs = self.docs
        if (docs is not None):
            hash_value ^= hash(docs)
        
        # attribute_name
        attribute_name = self.attribute_name
        if (attribute_name is not None):
            hash_value ^= hash(attribute_name)
        
        # type_name
        type_name = self.type_name
        if (type_name is not None):
            hash_value ^= hash(type_name)
        
        return hash_value
    
    
    def __set_name__(self, owner, attribute_name):
        """
        Called when the type is constructed.
        
        Parameters
        ----------
        owner : `type`
            The parent type.
        
        attribute_name : `str`
            the name of the help attribute.
        """
        self.type_name = owner.__name__
        self.attribute_name = attribute_name
    
    
    def __get__(self, instance, type_):
        """
        Called when the place holder is accessed with a `get` operation.
        
        Returns
        -------
        self / default : `self` / `object`
            If accessed from class returns self. If from instance, returns the default object.
        """
        if instance is None:
            return self
        
        return NotImplemented
    
    
    def __set__(self, instance, value):
        """
        Called when place holder is accessed with a `set` operation.
        
        Raises
        ------
        NotImplementedError
        """
        if instance is None:
            type_name = self.type_name
        else:
            type_name = type(instance).__name__
        
        attribute_name = self.attribute_name
        if attribute_name is None:
            attribute_name = 'unknown'
        
        raise NotImplementedError(
            f'Setting `{type_name}.{attribute_name}` is not supported; '
            f'got instance = {instance!r}; value = {value!r}.'
        )
    
    
    def __delete__(self, instance):
        """
        Called when place holder is accessed with a `del` operation.
        
        Raises
        ------
        NotImplementedError
        """
        if instance is None:
            type_name = self.type_name
        else:
            type_name = type(instance).__name__
        
        attribute_name = self.attribute_name
        if attribute_name is None:
            attribute_name = 'unknown'
        
        raise NotImplementedError(
            f'Deleting `{type_name}.{attribute_name}` is not supported; '
            f'got instance = {instance!r}.'
        )
