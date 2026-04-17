__all__ = ('InteractionComponentMetadataLabel',)

from scarletio import copy_docs

from .base import InteractionComponentMetadataBase
from .fields import parse_component, put_component, validate_component__label


class InteractionComponentMetadataLabel(InteractionComponentMetadataBase):
    """
    Interaction component metadata representing a label component.
    
    Attributes
    ----------
    component : ``None | InteractionComponent``
        Sub-component nested inside.
    """
    __slots__ = ('component', )
    
    def __new__(cls, *, component = ...):
        """
        Creates a new interaction component metadata from the given fields.
        
        Parameters
        ----------
        component : ``None | InteractionComponent``, Optional (Keyword only)
            Sub-component nested inside.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # component
        if component is ...:
            component = None
        else:
            component = validate_component__label(component)
        
        # Construct.
        self = object.__new__(cls)
        self.component = component
        return self
    
    
    @classmethod
    def from_keyword_parameters(cls, keyword_parameters):
        """
        Creates a new interaction component metadata from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict<str, object>`
            Keyword parameters to build the metadata from.
        
        Returns
        -------
        self : `instance<type<cls>>`
        
        Raises
        ------
        TypeError
            - If a keyword parameter's type is incorrect.
        ValueError
            - If a keyword parameter's value is incorrect.
        """
        return cls(
            component = keyword_parameters.pop('component', ...),
        )
    
    
    @copy_docs(InteractionComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # component
        repr_parts.append(' component = ')
        repr_parts.append(repr(self.component))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(InteractionComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # component
        component = self.component
        if (component is not None):
            hash_value ^= hash(component)
        
        return hash_value
    
    
    @copy_docs(InteractionComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # component
        if self.component != other.component:
            return False
        
        return True
    
    
    @copy_docs(InteractionComponentMetadataBase._match_to_component)
    def _match_to_component(self, other):
        # component
        self_component = self.component
        other_component = other.component
        
        if (self_component is None) != (other_component is None):
            return False
        
        if (self_component is not None) and (not (self_component % other_component)):
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(InteractionComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.component = parse_component(data)
        return self
    
    
    @copy_docs(InteractionComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_component(self.component, data, defaults)
        return data
    
    
    @copy_docs(InteractionComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # component
        component = self.component
        if (component is not None):
            component = component.copy()
        new.component = component
        
        return new
    
    
    def copy_with(self, *, component = ...,):
        """
        Copies the interaction component metadata with the given fields.
        
        Parameters
        ----------
        component : ``None | InteractionComponent``, Optional (Keyword only)
            Sub-component nested inside.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """
        # component
        if component is ...:
            component = self.component
            if (component is not None):
                component = component.copy()
        else:
            component = validate_component__label(component)
        
        # Construct.
        new = object.__new__(type(self))
        new.component = component
        return new
    
    
    @copy_docs(InteractionComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            component = keyword_parameters.pop('component', ...),
        )
    
    
    @copy_docs(InteractionComponentMetadataBase.iter_custom_ids_and_values)
    def iter_custom_ids_and_values(self):
        component = self.component
        if (component is not None):
            yield from component.iter_custom_ids_and_values()
