__all__ = ()

from ...field_parsers import nullable_string_parser_factory
from ...field_putters import nullable_string_optional_putter_factory
from ...field_validators import nullable_string_validator_factory

from ..component import Component, ComponentType, ComponentTypeLayoutFlag
from ..shared_fields import parse_components, parse_custom_id, put_components, put_custom_id, validate_custom_id

from .constants import TITLE_LENGTH_MAX, TITLE_LENGTH_MIN


COMPONENT_TYPE_LAYOUT_FLAG_TOP_LEVEL = ComponentTypeLayoutFlag().update_by_keys(top_level = True)
COMPONENT_TYPE_LAYOUT_FLAG_ALLOWED_IN_FORM = ComponentTypeLayoutFlag().update_by_keys(allowed_in_form = True)


# components

def validate_components(components):
    """
    Interaction form specific component validator.
    
    Parameters
    ----------
    components : ``None | iterable<Component | (tuple | list)<Component>>``
        The components to validate.
    
    Returns
    -------
    components : ``None | tuple<Component>``
    
    Raises
    ------
    TypeError
        - If `components` is invalid type.
    ValueError
        - If `components` contains an invalid value.
    """
    if components is None:
        return None
    
    if (getattr(components, '__iter__', None) is None):
        raise TypeError(
            f'`components` can be `None`, `iterable` of `{Component.__name__}`, got '
            f'{type(components).__name__}; {components!r}.'
        )
        
    components_processed = None
    
    for component in components:
        if not isinstance(component, Component):
            raise TypeError(
                f'`components` can contain `{Component.__name__}` elements, got '
                f'{type(component).__name__}; {component!r}; components = {components!r}.'
            )
        
        flags = component.type.layout_flags
        if not flags & COMPONENT_TYPE_LAYOUT_FLAG_ALLOWED_IN_FORM:
            raise ValueError(
                f'Component {component!r} is not allowed to be in a form.',
            )
        
        if not flags & COMPONENT_TYPE_LAYOUT_FLAG_TOP_LEVEL:
            component = Component(ComponentType.row, components = [component])
        
        if (components_processed is None):
            components_processed = []
        
        components_processed.append(component)
    
    if (components_processed is not None):
        components_processed = tuple(components_processed)
    
    return components_processed


# title

parse_title = nullable_string_parser_factory('title')
put_title = nullable_string_optional_putter_factory('title')
validate_title = nullable_string_validator_factory('title', TITLE_LENGTH_MIN, TITLE_LENGTH_MAX)
