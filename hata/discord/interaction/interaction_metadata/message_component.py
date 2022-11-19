__all__ = ('InteractionMetadataMessageComponent',)

import warnings

from scarletio import copy_docs

from ...component import Component, ComponentType

from .base import InteractionMetadataBase
from .fields import (
    parse_component_type, parse_custom_id, parse_resolved, parse_values, put_component_type_into, put_custom_id_into,
    put_resolved_into, put_values_into, validate_component_type, validate_custom_id, validate_resolved, validate_values
)


class InteractionMetadataMessageComponent(InteractionMetadataBase):
    """
    Interaction metadata used when the interaction was triggered by an application command's auto completion.
    
    Parameters
    ----------
    component_type : ``ComponentType``
        The used component's type.
    
    custom_id : `None`, `str`
        Component or form interaction's custom identifier.
    
    resolved : `None`, ``Resolved``
        Contains the received entities.
    
    values : `None`, `tuple` of `str`
        Values selected by the user.
    """
    __slots__ = ('component_type', 'custom_id', 'resolved', 'values')
    
    @classmethod
    @copy_docs(InteractionMetadataBase._create_empty)
    def _create_empty(cls):
        self = object.__new__(cls)
        self.component_type = ComponentType.none
        self.custom_id = None
        self.resolved = None
        self.values = None
        return self
    
    
    @copy_docs(InteractionMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.component_type = self.component_type
        new.custom_id = self.custom_id
        
        resolved = self.resolved
        if (resolved is not None):
            resolved = resolved.copy()
        new.resolved = resolved
        
        values = self.values
        if (values is not None):
            values = (*values,)
        new.values = values
        
        return new
    
    
    @copy_docs(InteractionMetadataBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        # component_type
        try:
            component_type = keyword_parameters.pop('component_type')
        except KeyError:
            pass
        else:
            self.component_type = validate_component_type(component_type)
        
        # custom_id
        try:
            custom_id = keyword_parameters.pop('custom_id')
        except KeyError:
            pass
        else:
            self.custom_id = validate_custom_id(custom_id)
        
        # resolved
        try:
            resolved = keyword_parameters.pop('resolved')
        except KeyError:
            pass
        else:
            self.resolved = validate_resolved(resolved)
        
        # values
        try:
            values = keyword_parameters.pop('values')
        except KeyError:
            pass
        else:
            self.values = validate_values(values)
        
        
        InteractionMetadataBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase.from_data)
    def from_data(cls, data, interaction_event):
        self = object.__new__(cls)
        self.component_type = parse_component_type(data)
        self.custom_id = parse_custom_id(data)
        self.resolved = parse_resolved(data, interaction_event)
        self.values = parse_values(data)
        return self
    
    
    @copy_docs(InteractionMetadataBase.to_data)
    def to_data(self, *, defaults = False, interaction_event = None):
        data = {}
        put_component_type_into(self.component_type, data, defaults)
        put_custom_id_into(self.custom_id, data, defaults)
        put_resolved_into(self.resolved, data, defaults, interaction_event = interaction_event)
        put_values_into(self.values, data, defaults)
        return data
    
    
    @copy_docs(InteractionMetadataBase._put_attribute_representations_into)
    def _put_attribute_representations_into(self, repr_parts):
        # component_type
        repr_parts.append(' component_type = ')
        repr_parts.append(repr(self.component_type))
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id = ')
            repr_parts.append(repr(custom_id))
        
        # resolved
        resolved = self.resolved
        if (resolved is not None):
            repr_parts.append(', resolved = ')
            repr_parts.append(repr(resolved))
        
        # values
        values = self.values
        if (values is not None):
            repr_parts.append(', values = ')
            repr_parts.append(repr(values))
        
        return True
    
    
    @copy_docs(InteractionMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # component_type
        hash_value ^= self.component_type.value
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(self.custom_id)
        
        # resolved
        resolved = self.resolved
        if (resolved is not None):
            hash_value ^= hash(resolved)
        
        # values
        values = self.values
        if (values is not None):
            hash_value ^= len(values)
            
            for option in values:
                hash_value ^= hash(option)
        
        return hash_value
    
    
    @copy_docs(InteractionMetadataBase.__eq__)
    def __eq__(self, other):
        other_type = type(other)
        if other_type is type(self):
            return self._is_equal_same_type(other)
        
        # Compare with components.
        if issubclass(other_type, Component):
            # Check `type` before `custom_id`
            
            # type
            if self.component_type is not other.type:
                return False
            
            # custom_id
            if self.custom_id != other.custom_id:
                return False
            
            return True
        
        return NotImplemented
    
    
    @copy_docs(InteractionMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # component_type
        if self.component_type is not other.component_type:
            return False
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # resolved
        if self.resolved != other.resolved:
            return False
        
        # values
        if self.values != other.values:
            return False
        
        return True
    
    
    @property
    def options(self):
        """
        At the case of ``InteractionMetadataMessageComponent`` instances ``.options`` is deprecated and will be removed
        in 2023 February. Please use ``.values``.
        
        If you are accessing this field as a proxied attribute, you can ignore this warning.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.options` is deprecated and will be removed in 2023 February. '
                f'Please use `.values` instead. If you are accessing this field as a proxied attribute, '
                f'you can ignore this warning.'
            ),
            stacklevel = 2,
        )
        
        return self.values
    
    
    @property
    def type(self):
        """
        ``InteractionMetadataMessageComponent.type`` is deprecated and will be removed in 2023 February.
        Please use ``.component_type``.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.type` is deprecated and will be removed in 2023 February. '
                f'Please use `.component_type` instead.'
            ),
            stacklevel = 2,
        )
        
        return self.component_type
