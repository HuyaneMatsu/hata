__all__ = ()

from scarletio import include_with_callback

from ..emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data
from ..field_parsers import (
    nullable_functional_parser_factory, nullable_object_array_parser_factory, nullable_string_parser_factory
)
from ..field_putters import (
    nullable_entity_array_putter_factory, nullable_functional_optional_putter_factory, url_optional_putter_factory
)
from ..field_validators import nullable_entity_validator_factory, nullable_string_validator_factory

from .shared_constants import CUSTOM_ID_LENGTH_MAX

# components

parse_components = nullable_object_array_parser_factory('components', NotImplemented, include = 'Component')
put_components = nullable_entity_array_putter_factory(
    'components', NotImplemented, can_include_internals = True, include = 'Component'
)

def validate_components_factory(nesting_target_name, allowed_in_name, allowed_in_flag_names, any_required_flag_names):
    """
    Creates a new component validator.
    
    Parameters
    ----------
    nesting_target_name : `int`
        The name under what these components will be nested to.
    
    allowed_in_name : `str`
        The name of the location where the items must be allowed.
    
    allowed_in_flag_names : `tuple<str>`
        Where the items must be allowed. Keys to pass as `True` to ``ComponentTypeLayoutFlag.update_by_keys``.
    
    any_required_flag_names : `tuple<str>`
        Required layout flags. Keys to pass as `True` to ``ComponentTypeLayoutFlag.update_by_keys``.
        
        Note that only non-strict matching is supported by the generated function.
    
    Returns
    -------
    validator : ``(None | iterable<Component | (tuple | list)<Component>>) -> None | tuple<Component>``
    """
    COMPONENT_LAYOUT_MASK_ANY_REQUIRED = 0
    COMPONENT_LAYOUT_FLAG_NESTABLE_INTO_ROW = 0
    COMPONENT_LAYOUT_FLAG_ROW = 0
    COMPONENT_LAYOUT_FLAG_ALLOWED_IN = 0
    NESTING_INTO_ROW_ALLOWED = False
    ComponentType = NotImplemented
    Component = NotImplemented
    
    def validator(components):
        """
        Validates the given components and whether they can be nested into a certain other component.
        
        This function is auto generated.
        
        Parameters
        ----------
        components : ``None | iterable<Component | (tuple | list)<Component>>``
            The components to validate.
        
        Returns
        -------
        components_processed : ``None | tuple<Component>``
        
        Raises
        ------
        TypeError
            - If `components` is invalid type.
        ValueError
            - If any of the `components` cannot be nested.
        """
        nonlocal nesting_target_name
        nonlocal COMPONENT_LAYOUT_MASK_ANY_REQUIRED
        nonlocal COMPONENT_LAYOUT_FLAG_NESTABLE_INTO_ROW
        nonlocal COMPONENT_LAYOUT_FLAG_ROW
        nonlocal COMPONENT_LAYOUT_FLAG_ALLOWED_IN
        nonlocal ComponentType
        nonlocal Component
        nonlocal allowed_in_name
        nonlocal NESTING_INTO_ROW_ALLOWED
        
        if components is None:
            return None
        
        if (getattr(components, '__iter__', None) is None):
            raise TypeError(
                f'`components` can be `None`, `iterable` of `{Component.__name__}`, got '
                f'{type(components).__name__}; {components!r}.'
            )
        
        components_processed = None
        
        for component in components:
            if isinstance(component, Component):
                flags = component.type.layout_flags
                if not (flags & COMPONENT_LAYOUT_FLAG_ALLOWED_IN):
                    raise ValueError(
                        f'Cannot use components of type {component.type.name} in {allowed_in_name}, '
                        f'got {component!r}; components = {components!r}.'
                    )
                
                if (flags & COMPONENT_LAYOUT_MASK_ANY_REQUIRED):
                    # Allow any component satisfying the flag.
                    pass
                
                elif (
                    NESTING_INTO_ROW_ALLOWED and
                    (COMPONENT_LAYOUT_FLAG_ROW & COMPONENT_LAYOUT_MASK_ANY_REQUIRED) and
                    (flags & COMPONENT_LAYOUT_FLAG_NESTABLE_INTO_ROW)
                ):
                    # If the component is nestable to a row and we are not nesting to a row currently,
                    # wrap the component into a row automatically.
                    component = Component(
                        ComponentType.row,
                        components = (component,),
                    )
                    
                else:
                    raise ValueError(
                        f'Cannot nest components of type {component.type.name} into a {nesting_target_name!s} '
                        f'in a {allowed_in_name}, got {component!r}; components = {components!r}.'
                    )
            
            elif (
                isinstance(component, list) or isinstance(component, tuple) and
                all(isinstance(nested_component, Component) for nested_component in component)
            ):
                if (
                    NESTING_INTO_ROW_ALLOWED and
                    (COMPONENT_LAYOUT_FLAG_ROW & COMPONENT_LAYOUT_MASK_ANY_REQUIRED) and
                    all(
                        nested_component.type.layout_flags & COMPONENT_LAYOUT_FLAG_NESTABLE_INTO_ROW
                        for nested_component in component
                    )
                ):
                    # nest components into a row if all can be nested and nesting is supported.
                    component = Component(
                        ComponentType.row,
                        components = component,
                    )
                
                else:
                    raise ValueError(
                        f'Either nesting into a row is not allowed or at least one component cannot be nested int a '
                        f'row, got {component!r}; components = {components!r}.',
                    )
            
            else:
                raise TypeError(
                    f'`components` can contain `{Component.__name__}` elements, got '
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
        nonlocal COMPONENT_LAYOUT_FLAG_NESTABLE_INTO_ROW
        nonlocal allowed_in_flag_names
        nonlocal COMPONENT_LAYOUT_FLAG_ALLOWED_IN
        nonlocal NESTING_INTO_ROW_ALLOWED
        
        COMPONENT_LAYOUT_MASK_ANY_REQUIRED = resolved_ComponentTypeLayoutFlag().update_by_keys(
            **dict.fromkeys(any_required_flag_names, True)
        )
        COMPONENT_LAYOUT_FLAG_ALLOWED_IN = resolved_ComponentTypeLayoutFlag().update_by_keys(
            **dict.fromkeys(allowed_in_flag_names, True)
        )
        COMPONENT_LAYOUT_FLAG_NESTABLE_INTO_ROW = resolved_ComponentTypeLayoutFlag().update_by_keys(
            nestable_into_row = True
        )
        NESTING_INTO_ROW_ALLOWED = not COMPONENT_LAYOUT_MASK_ANY_REQUIRED & COMPONENT_LAYOUT_FLAG_NESTABLE_INTO_ROW
    
    
    @include_with_callback('ComponentType')
    def include_component_type(resolved_ComponentType):
        nonlocal COMPONENT_LAYOUT_FLAG_ROW
        nonlocal ComponentType
        
        ComponentType = resolved_ComponentType
        COMPONENT_LAYOUT_FLAG_ROW = resolved_ComponentType.row.layout_flags
    
    
    @include_with_callback('Component')
    def include_component(resolved_Component):
        nonlocal Component
        
        Component = resolved_Component
    
    
    return validator


validate_components = validate_components_factory(
    'row / container',
    'message',
    (
        'allowed_in_message',
    ),
    (
        'nestable_into_row',
        'nestable_into_container',
        'nestable_into_section',
    ),
)


# custom_id

parse_custom_id = nullable_string_parser_factory('custom_id')
put_custom_id = url_optional_putter_factory('custom_id')
validate_custom_id = nullable_string_validator_factory('custom_id', 0, CUSTOM_ID_LENGTH_MAX)

# emoji

parse_emoji = nullable_functional_parser_factory('emoji', create_partial_emoji_from_data)
put_emoji = nullable_functional_optional_putter_factory('emoji', create_partial_emoji_data)
validate_emoji = nullable_entity_validator_factory('emoji', Emoji)
