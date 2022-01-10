__all__ = ('ComponentBase',)

from scarletio import RichAttributeErrorBaseType, export

from .preinstanced import ComponentType


@export
class ComponentBase(RichAttributeErrorBaseType):
    """
    Base class for 3rd party components.
    
    Class Attributes
    ----------------
    custom_id : `NoneType` = `None`
        Placeholder for sub-classes without `custom_id` attribute.
    type : ``ComponentType`` = `ComponentType.none`
        The component's type.
    """
    __slots__ = ()
    
    custom_id = None
    type = ComponentType.none
    
    def __new__(cls):
        """
        Creates a component base instance.
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new message component from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message component data.
        
        Returns
        -------
        self : ``ComponentBase``
            The created component instance.
        """
        return None
    
    
    def to_data(self):
        """
        Converts the component to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        # type
        data = {
            'type' : self.type.value
        }
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            data['custom_id'] = custom_id
        
        return data
    
    
    def __repr__(self):
        """Returns the message component's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def copy(self):
        """
        Copies the component.
        
        Returns
        -------
        new : ``ComponentBase``
        """
        return self
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        """
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
        return self
    
    
    def __eq__(self, other):
        """Returns Whether the two component are equal."""
        if type(other) is not type(self):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the component's hash value."""
        return self.type.value
    
    
    def _iter_components(self):
        """
        Iterates over the sub-components recursively of the component including itself.
        
        This method is a generator.
        
        Yields
        ------
        component : ``ComponentBase``
        """
        yield self
        return
    
    
    def _replace_direct_sub_components(self, relation):
        """
        Replaces the sub components of the component with the given relation.
        
        Parameters
        ----------
        relation : `dict` of (``ComponentBase``, ``ComponentBase``) items
            Relation to replace each component with.
        """
        pass
    
    
    def _iter_direct_sub_components(self):
        """
        Iterates over the sub-components of the component.
        
        This method is a generator.
        
        Yields
        ------
        component : ``ComponentBase``
        """
        return
        yield
