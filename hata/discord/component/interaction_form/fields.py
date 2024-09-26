__all__ = ()

from ...field_parsers import nullable_string_parser_factory
from ...field_putters import nullable_string_optional_putter_factory
from ...field_validators import nullable_string_validator_factory

from ..component import Component, ComponentType

from .constants import TITLE_LENGTH_MIN, TITLE_LENGTH_MAX

# components

def validate_components(components):
    """
    Interaction form specific component validator.
    
    Parameters
    ----------
    components : `None | iterable<Component>`
        The components to validate.
    
    Returns
    -------
    components : `None | tuple<Component>`
    
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
        
        if not component.type.layout_flags.top_level:
            component = Component(ComponentType.row, components = [component])
        
        if (components_processed is None):
            components_processed = []
        
        components_processed.append(component)
    
    if (components_processed is not None):
        components_processed = tuple(components_processed)
    
    return components_processed


# title

parse_title = nullable_string_parser_factory('title')
put_title_into = nullable_string_optional_putter_factory('title')
validate_title = nullable_string_validator_factory('title', TITLE_LENGTH_MIN, TITLE_LENGTH_MAX)
