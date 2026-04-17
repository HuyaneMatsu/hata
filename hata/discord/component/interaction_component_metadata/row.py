__all__ = ('InteractionComponentMetadataRow',)

from scarletio import copy_docs

from .base import InteractionComponentMetadataBase
from .fields import parse_components, put_components, validate_components__row


class InteractionComponentMetadataRow(InteractionComponentMetadataBase):
    """
    Interaction component metadata representing a row component.
    
    Attributes
    ----------
    components : ``None | tuple<InteractionComponent>``
        Sub-components nested inside.
    """
    __slots__ = ('components', )
    
    def __new__(cls, *, components = ...):
        """
        Creates a new interaction component metadata from the given fields.
        
        Parameters
        ----------
        components : ``None | iterable<InteractionComponent>``, Optional (Keyword only)
            Sub-components nested inside.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # components
        if components is ...:
            components = None
        else:
            components = validate_components__row(components)
        
        # Construct.
        self = object.__new__(cls)
        self.components = components
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
            components = keyword_parameters.pop('components', ...),
        )
    
    
    @copy_docs(InteractionComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # components
        repr_parts.append(' components = ')
        repr_parts.append(repr(self.components))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(InteractionComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components)
            
            for component in components:
                hash_value ^= hash(component)
        
        return hash_value
    
    
    @copy_docs(InteractionComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # components
        if self.components != other.components:
            return False
        
        return True
    
    
    @copy_docs(InteractionComponentMetadataBase._match_to_component)
    def _match_to_component(self, other):
        # components
        self_components = self.components
        other_components = other.components
        
        if (self_components is None) != (other_components is None):
            return False
        
        if (
            (self_components is not None) and
            (
                (len(self_components) != len(other_components)) or
                (not all(
                    self_component % other_component
                    for self_component, other_component
                    in zip(self_components, other_components)
                ))
            )
        ):
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(InteractionComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.components = parse_components(data)
        return self
    
    
    @copy_docs(InteractionComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_components(self.components, data, defaults)
        return data
    
    
    @copy_docs(InteractionComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # components
        components = self.components
        if (components is not None):
            components = (*(component.copy() for component in components),)
        new.components = components
        
        return new
    
    
    def copy_with(self, *, components = ...):
        """
        Copies the interaction component metadata with the given fields.
        
        Parameters
        ----------
        components : ``None | iterable<InteractionComponent>``, Optional (Keyword only)
            Sub-components nested inside.
        
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
        # components
        if components is ...:
            components = self.components
            if (components is not None):
                components = (*(component.copy() for component in components),)
        else:
            components = validate_components__row(components)
        
        # Construct.
        new = object.__new__(type(self))
        new.components = components
        return new
    
    
    @copy_docs(InteractionComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            components = keyword_parameters.pop('components', ...),
        )
    
    
    @copy_docs(InteractionComponentMetadataBase.iter_custom_ids_and_values)
    def iter_custom_ids_and_values(self):
        components = self.components
        if (components is not None):
            for component in components:
                yield from component.iter_custom_ids_and_values()
