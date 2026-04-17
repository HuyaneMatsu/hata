__all__ = ('InteractionComponentMetadataContainer',)

from scarletio import copy_docs

from .row import InteractionComponentMetadataRow
from .fields import validate_components__container


class InteractionComponentMetadataContainer(InteractionComponentMetadataRow):
    """
    Interaction component metadata representing a container component.
    
    Attributes
    ----------
    components : ``None | tuple<InteractionComponent>``
        Sub-components nested inside.
    """
    __slots__ = ()
    
    @copy_docs(InteractionComponentMetadataRow.__new__)
    def __new__(cls, *, components = ...):
        # components
        if components is ...:
            components = None
        else:
            components = validate_components__container(components)
        
        # Construct.
        self = object.__new__(cls)
        self.components = components
        return self
    
    
    @copy_docs(InteractionComponentMetadataRow.copy_with)
    def copy_with(self, *, components = ...):
        # components
        if components is ...:
            components = self.components
            if (components is not None):
                components = (*(component.copy() for component in components),)
        else:
            components = validate_components__container(components)
        
        # Construct.
        new = object.__new__(type(self))
        new.components = components
        return new
