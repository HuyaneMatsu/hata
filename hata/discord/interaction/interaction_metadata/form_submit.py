__all__ = ('InteractionMetadataFormSubmit',)

import warnings

from scarletio import copy_docs

from .base import InteractionMetadataBase
from .fields import (
    parse_custom_id, parse_components, put_custom_id_into, put_components_into, validate_custom_id, validate_components
)


class InteractionMetadataFormSubmit(InteractionMetadataBase):
    """
    Interaction metadata used when the interaction was triggered by an application command's auto completion.
    
    Parameters
    ----------
    components : `None`, `tuple` of ``InteractionComponent``
        Submitted component values of a form submit interaction.
    
    custom_id : `None`, `str`
        Component or form interaction's custom identifier.
    """
    __slots__ = ('components', 'custom_id')
    
    @classmethod
    @copy_docs(InteractionMetadataBase._create_empty)
    def _create_empty(cls):
        self = object.__new__(cls)
        self.components = None
        self.custom_id = None
        return self
    
    
    @copy_docs(InteractionMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        components = self.components
        if (components is not None):
            components = tuple(option.copy() for option in components)
        new.components = components
        
        new.custom_id = self.custom_id
        
        return new
    
    
    @copy_docs(InteractionMetadataBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        # components
        try:
            components = keyword_parameters.pop('components')
        except KeyError:
            pass
        else:
            self.components = validate_components(components)
        
        # custom_id
        try:
            custom_id = keyword_parameters.pop('custom_id')
        except KeyError:
            pass
        else:
            self.custom_id = validate_custom_id(custom_id)
        
        InteractionMetadataBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase.from_data)
    def from_data(cls, data, interaction_event):
        self = object.__new__(cls)
        self.components = parse_components(data)
        self.custom_id = parse_custom_id(data)
        return self
    
    
    @copy_docs(InteractionMetadataBase.to_data)
    def to_data(self, *, defaults = False, interaction_event = None):
        data = {}
        put_components_into(self.components, data, defaults)
        put_custom_id_into(self.custom_id, data, defaults)
        return data
    
    
    @copy_docs(InteractionMetadataBase._put_attribute_representations_into)
    def _put_attribute_representations_into(self, repr_parts):
        
        # components
        components = self.components
        if (components is not None):
            repr_parts.append(' components = ')
            repr_parts.append(repr(components))
            
            field_added = False
        else:
            field_added = True
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' custom_id = ')
            repr_parts.append(repr(custom_id))
        
        return field_added
    
    
    @copy_docs(InteractionMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components)
            
            for option in components:
                hash_value ^= hash(option)
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        return hash_value
    
    
    @copy_docs(InteractionMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # components
        if self.components != other.components:
            return False
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        return True
    
    
    @property
    def options(self):
        """
        At the case of ``InteractionMetadataFormSubmit`` instances ``.components`` is deprecated and will be removed
        in 2023 February. Please use ``.components``.
        
        If you are accessing this field as a proxied attribute, you can ignore this warning.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.components` is deprecated and will be removed in 2023 February. '
                f'Please use `.components` instead. If you are accessing this field as a proxied attribute, '
                f'you can ignore this warning.'
            )
        )
        
        return self.components
