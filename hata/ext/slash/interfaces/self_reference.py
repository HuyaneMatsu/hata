__all__ = ()

from scarletio import RichAttributeErrorBaseType, WeakReferer


def get_self_reference_of(instance):
    """
    Gets self reference of the given instance.
    
    Parameters
    ----------
    instance : `None | SelfReferenceInterface | object`
        Instance to get self reference of.
    
    Returns
    -------
    self_reference: `None | WeakReferer`
    """
    if instance is None:
        return None
    
    if isinstance(instance, SelfReferenceInterface):
        return instance.get_self_reference()
    
    return None


class SelfReferenceInterface(RichAttributeErrorBaseType):
    """
    Base class for types supporting self-reference getting.
    """
    __slots__ = ()
    
    def get_self_reference(self):
        """
        Gets a weak reference to the instance.
        
        Returns
        -------
        self_reference : `WeakReferer<self>`
        """
        self_reference = self._self_reference
        if self_reference is None:
            try:
                self_reference = WeakReferer(self)
            except TypeError:
                self_reference = None
            else:
                self._self_reference = self_reference
        
        return self_reference
    
    
    @property
    def _self_reference(self):
        """
        The registered self-reference.
        
        Returns
        -------
        self_reference : `None | WeakReferer`
        """
        return None
    
    
    @_self_reference.setter
    def _self_reference(self, value):
        pass
