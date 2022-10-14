__all__ = ('PlaceHolder',)

from scarletio import docs_property


class PlaceHolder:
    __class_doc__ = (
    """
    Slot place holder returning a default value.
    
    Might be used to avoid `__getattr__` definitions.
    
    Attributes
    ----------
    default : `object`
        The object to return from getter.
    docs : `None`, `str`
        Documentation of the place held attribute.
    name : `None, `str`
        The name of the place held attribute.
    """)
    
    @property
    def __instance_doc__(self):
        return self.docs
    
    __doc__ = docs_property()
    
    __slots__ = ('default', 'docs', 'name')
    
    
    def __new__(cls, default, docs = None):
        """
        Creates a new new slot place holder.
        
        Parameters
        ----------
        default : `object`
            The object to return from getter.
        docs : `None`, `str` = `None`, Optional
            Documentation of the place held attribute.
        """
        self = object.__new__(cls)
        self.default = default
        self.docs = docs
        self.name = None
        return self
    

    def __set_name__(self, owner, name):
        """
        Called when the type is constructed.
        
        Parameters
        ----------
        owner : `type`
            The parent type.
        name : `str`
            the name of the help attribute.
        """
        self.name = name
    
    
    def __get__(self, instance, type_):
        """
        Called when the place holder is accessed with a `get` operation.
        
        Returns
        -------
        self / default : ``PlaceHolder`` / `object`
            If accessed from class returns self. If from instance, returns the default object.
        """
        if instance is None:
            return self
        
        return self.default
    
    
    def __set__(self, instance, value):
        """
        Called when place holder is accessed with a `set` operation.
        
        Raises
        ------
        NotImplementedError
        """
        name = self.name
        if name is None:
            name = 'unknown'
        else:
            name = repr(name)
        
        raise NotImplementedError(
            f'Setting {name} attribute of {instance.__class__} is not supported; '
            f'got instance={instance!r}; value={value!r}.'
        )
    
    
    def __delete__(self, instance):
        """
        Called when place holder is accessed with a `del` operation.
        
        Raises
        ------
        NotImplementedError
        """
        name = self.name
        if name is None:
            name = 'unknown'
        else:
            name = repr(name)
        
        raise NotImplementedError(
            f'Deleting {name} attribute of {instance.__class__} is not supported; '
            f'got instance={instance!r}.'
        )
