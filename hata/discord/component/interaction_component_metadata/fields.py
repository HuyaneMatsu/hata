__all__ = ()

from scarletio import include, include_with_callback

from ...field_parsers import (
    field_parser_factory, nullable_array_parser_factory, nullable_entity_parser_factory,
    nullable_object_array_parser_factory
)
from ...field_putters import (
    nullable_entity_optional_putter_factory, nullable_object_array_optional_putter_factory,
    nullable_string_array_optional_putter_factory, nullable_string_optional_putter_factory
)
from ...field_validators import (
    nullable_entity_validator_factory, nullable_object_array_validator_factory,
    nullable_string_array_validator_factory, nullable_string_validator_factory
)

from ..shared_fields import parse_custom_id, put_custom_id, validate_custom_id

# components

InteractionComponent = include('InteractionComponent')


def validate_components_factory(nesting_target_name, any_required_flag_names):
    """
    Creates a new component validator.
    
    Parameters
    ----------
    nesting_target_name : `int`
        The name under what these components will be nested to.
    
    any_required_flag_names : `tuple<str>`
        Required layout flags. Keys to pass as `True` to ``ComponentTypeLayoutFlag.update_by_keys``.
        
        Note that only non-strict matching is supported by the generated function.
    
    Returns
    -------
    validator : ``(None | iterable<InteractionComponent>) -> None | tuple<InteractionComponent>``
    """
    COMPONENT_LAYOUT_MASK_ANY_REQUIRED = 0
    InteractionComponent = NotImplemented
    
    def validator(components):
        """
        Validates the given components and whether they can be nested into a certain other component.
        
        This function is auto generated.
        
        Parameters
        ----------
        components : ``None | iterable<InteractionComponent | (tuple | list)<InteractionComponent>>``
            The components to validate.
        
        Returns
        -------
        components_processed : ``None | tuple<InteractionComponent>``
        
        Raises
        ------
        TypeError
            - If `components` is invalid type.
        ValueError
            - If any of the `components` cannot be nested.
        """
        nonlocal nesting_target_name
        nonlocal COMPONENT_LAYOUT_MASK_ANY_REQUIRED
        nonlocal InteractionComponent
        
        if components is None:
            return None
        
        if (getattr(components, '__iter__', None) is None):
            raise TypeError(
                f'`components` can be `None`, `iterable` of `{InteractionComponent.__name__}`, got '
                f'{type(components).__name__}; {components!r}.'
            )
        
        components_processed = None
        
        for component in components:
            if isinstance(component, InteractionComponent):
                flags = component.type.layout_flags
                if (flags & COMPONENT_LAYOUT_MASK_ANY_REQUIRED):
                    # Allow any component satisfying the flag.
                    pass
                    
                else:
                    raise ValueError(
                        f'Cannot nest components of type {component.type.name} into a {nesting_target_name!s}'
                        f', got {component!r}; components = {components!r}.'
                    )
            
            else:
                raise TypeError(
                    f'`components` can contain `{InteractionComponent.__name__}` elements, got '
                    f'{type(component).__name__}; {component!r}; components = {components!r}.'
                )
            
            if (components_processed is None):
                components_processed = []
            
            components_processed.append(component)
        
        if (components_processed is not None):
            components_processed = tuple(components_processed)
        
        return components_processed
    
    
    @include_with_callback('ComponentTypeLayoutFlag')
    def include_component_type_layout_flag(resolved_ComponentTypeLayoutFlag):
        nonlocal any_required_flag_names
        nonlocal COMPONENT_LAYOUT_MASK_ANY_REQUIRED
        
        COMPONENT_LAYOUT_MASK_ANY_REQUIRED = resolved_ComponentTypeLayoutFlag().update_by_keys(
            **dict.fromkeys(any_required_flag_names, True)
        )
    
    
    @include_with_callback('InteractionComponent')
    def include_component(resolved_Component):
        nonlocal InteractionComponent
        
        InteractionComponent = resolved_Component
    
    
    return validator


parse_components = nullable_object_array_parser_factory('components', NotImplemented, include = 'InteractionComponent')
put_components = nullable_object_array_optional_putter_factory('components')

validate_components = nullable_object_array_validator_factory(
    'components', NotImplemented, include = 'InteractionComponent'
)

validate_components__row = validate_components_factory(
    'row',
    (
        'nestable_into_row',
    ),
)

validate_components__section = validate_components_factory(
    'section',
    (
        'nestable_into_section',
    ),
)

validate_components__container = validate_components_factory(
    'container',
    (
        'nestable_into_container',
    ),
)


# component

parse_component = nullable_entity_parser_factory('component', NotImplemented, include = 'InteractionComponent')
put_component = nullable_entity_optional_putter_factory('component', NotImplemented, can_include_internals = False)


def validate_component__label(component):
    """
    Validates whether the given label component is correct type.
    
    Parameters
    ----------
    component : ``None | InteractionComponent``
        The component to validate.
    
    Returns
    -------
    component : ``None | InteractionComponent``
    
    Raises
    ------
    TypeError
        - If `component` is given as an invalid type.
    """
    if component is None:
        return None
    
    if isinstance(component, InteractionComponent):
        if component.type.layout_flags.nestable_into_label:
            return component
        
        raise ValueError(
            f'Component of type: {component.type.name} cannot be used as a label component, got {component!r}.'
        )
    
    raise TypeError(
        f'`component` can be `{InteractionComponent.__name__}`, got {type(component).__name__}, {component!r}.'
    )


# thumbnail

parse_thumbnail = nullable_entity_parser_factory('thumbnail', NotImplemented, include = 'InteractionComponent')
put_thumbnail = nullable_entity_optional_putter_factory('thumbnail', NotImplemented, can_include_internals = False)


def validate_thumbnail(thumbnail):
    """
    Validates whether the given section thumbnail is correct type.
    
    Parameters
    ----------
    thumbnail : ``None | InteractionComponent``
        The thumbnail to validate.
    
    Returns
    -------
    thumbnail : ``None | InteractionComponent``
    
    Raises
    ------
    TypeError
        - If `thumbnail` is given as an invalid type.
    """
    if thumbnail is None:
        return None
    
    if isinstance(thumbnail, InteractionComponent):
        if thumbnail.type.layout_flags.section_thumbnail:
            return thumbnail
        
        raise ValueError(
            f'Component of type: {thumbnail.type.name} cannot be used as a section thumbnail, got {thumbnail!r}.'
        )
    
    raise TypeError(
        f'`thumbnail` can be `{InteractionComponent.__name__}`, got {type(thumbnail).__name__}, {thumbnail!r}.'
    )

# value

parse_value = field_parser_factory('value')
put_value = nullable_string_optional_putter_factory('value')
validate_value = nullable_string_validator_factory('value', 0, 16384)


# values

parse_values = nullable_array_parser_factory('values')
put_values = nullable_string_array_optional_putter_factory('values')
validate_values = nullable_string_array_validator_factory('values')
