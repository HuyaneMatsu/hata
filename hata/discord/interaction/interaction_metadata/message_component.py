__all__ = ('InteractionMetadataMessageComponent',)

from warnings import warn

from scarletio import copy_docs

from ...component import Component, ComponentType, InteractionComponent

from .base import InteractionMetadataBase
from .fields import parse_component, validate_component, put_component


class InteractionMetadataMessageComponent(InteractionMetadataBase):
    """
    Interaction metadata used when the interaction was triggered by an application command's auto completion.
    
    Attributes
    ----------
    component : ``None | InteractionComponent``
        The interacted interaction component.
    """
    __slots__ = ('component',)
    
    def __new__(
        cls,
        *,
        component = ...,
        component_type = ...,
        custom_id = ...,
        values = ...,
    ):
        """
        Creates a new interaction metadata from the given parameters.
        
        Parameters
        ----------
        component : ``None | InteractionComponent``, Optional (Keyword only)
            The interacted component.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # Deprecations
        if (component_type is not ...) or (custom_id is not ...) or (values is not ...):
            if (component_type is not ...):
                warn(
                    (
                        f'`{cls.__name__}.__new__`\'s `component_type` parameter is deprecated and is scheduled for '
                        f'removal at 2026 February. Please use the `component` parameter instead.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
            
            if (custom_id is not ...):
                warn(
                    (
                        f'`{cls.__name__}.__new__`\'s `custom_id` parameter is deprecated and is scheduled for '
                        f'removal at 2026 February. Please use the `component` parameter instead.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
            
            if (values is not ...):
                warn(
                    (
                        f'`{cls.__name__}.__new__`\'s `values` parameter is deprecated and is scheduled for '
                        f'removal at 2026 February. Please use the `component` parameter instead.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
            
            component = InteractionComponent(
                **{'component_type': ComponentType.string_select if component_type is ... else component_type},
                **({} if custom_id is ... else {'custom_id': custom_id}),
                **({} if values is ... else {'values': values}),
            )
        
        
        # component
        if component is ...:
            component = None
        else:
            component = validate_component(component)
        
        # Construct
        self = object.__new__(cls)
        self.component = component
        return self
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            component = keyword_parameters.pop('component', ...),
        )
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase._create_empty)
    def _create_empty(cls):
        self = object.__new__(cls)
        self.component = None
        return self
    
    
    @copy_docs(InteractionMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        component = self.component
        if (component is not None):
            component = component.copy()
        new.component = component
        
        return new
    
    
    def copy_with(
        self,
        *,
        component = ...,
        component_type = ...,
        custom_id = ...,
        values = ...,
    ):
        """
        Copies the interaction metadata with the given fields.
        
        Parameters
        ----------
        component : ``None | InteractionComponent``, Optional (Keyword only)
            The interacted component.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # Deprecations
        if (component_type is not ...) or (custom_id is not ...) or (values is not ...):
            if (component_type is not ...):
                warn(
                    (
                        f'`{type(self).__name__}.copy_with`\'s `component_type` parameter is deprecated and is '
                        f'scheduled for removal at 2026 February. Please use the `component` parameter instead.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
            
            if (custom_id is not ...):
                warn(
                    (
                        f'`{type(self).__name__}.copy_with`\'s `custom_id` parameter is deprecated and is scheduled '
                        f'for removal at 2026 February. Please use the `component` parameter instead.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
            
            if (values is not ...):
                warn(
                    (
                        f'`{type(self).__name__}.copy_with`\'s `values` parameter is deprecated and is scheduled for '
                        f'removal at 2026 February. Please use the `component` parameter instead.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
            
            component = InteractionComponent(
                **{'component_type': ComponentType.string_select if component_type is ... else component_type},
                **({} if custom_id is ... else {'custom_id': custom_id}),
                **({} if values is ... else {'values': values}),
            )
        
        # component
        if component is ...:
            component = self.component
            if (component is not None):
                component = component.copy()
        else:
            component = validate_component(component)
        
        # Construct
        new = object.__new__(type(self))
        new.component = component
        return new
    
    
    @copy_docs(InteractionMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            component = keyword_parameters.pop('component', ...),
        )
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase.from_data)
    def from_data(cls, data, guild_id = 0):
        self = object.__new__(cls)
        self.component = parse_component(data)
        return self
    
    
    @copy_docs(InteractionMetadataBase.to_data)
    def to_data(self, *, defaults = False, guild_id = 0):
        data = {}
        put_component(self.component, data, defaults)
        return data
    
    
    @copy_docs(InteractionMetadataBase._put_attribute_representations_into)
    def _put_attribute_representations_into(self, repr_parts):
        # component
        repr_parts.append(' component = ')
        repr_parts.append(repr(self.component))
        return True
    
    
    @copy_docs(InteractionMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # component
        hash_value ^= hash(self.component)
        
        return hash_value
    
    
    @copy_docs(InteractionMetadataBase.__eq__)
    def __eq__(self, other):
        other_type = type(other)
        if other_type is type(self):
            return self._is_equal_same_type(other)
        
        # Compare with components.
        if issubclass(other_type, Component):
            component = self.component
            if component is None:
                return False
            
            # Check `type` before `custom_id`
            
            # type
            if component.type is not other.type:
                return False
            
            # custom_id
            if component.custom_id != other.custom_id:
                return False
            
            return True
        
        return NotImplemented
    
    
    @copy_docs(InteractionMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # component
        if self.component != other.component:
            return False
        
        return True
    
    
    @copy_docs(InteractionMetadataBase.iter_custom_ids_and_values)
    def iter_custom_ids_and_values(self):
        component = self.component
        if (component is not None):
            yield from component.iter_custom_ids_and_values()
    
    
    @property
    @copy_docs(InteractionMetadataBase.custom_id)
    def custom_id(self):
        component = self.component
        if component is not None:
            return component.custom_id
