__all__ = ()

from scarletio import include

from ..emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data
from ..field_parsers import (
    nullable_functional_parser_factory, nullable_object_array_parser_factory, nullable_string_parser_factory
)
from ..field_putters import (
    nullable_entity_array_putter_factory, nullable_functional_optional_putter_factory, url_optional_putter_factory
)
from ..field_validators import (
    nullable_entity_validator_factory, nullable_object_array_validator_factory, nullable_string_validator_factory
)

from .shared_constants import CUSTOM_ID_LENGTH_MAX


Component = include('Component')


# components

parse_components = nullable_object_array_parser_factory('components', NotImplemented, include = 'Component')
put_components_into = nullable_entity_array_putter_factory('components', NotImplemented, include = 'Component')


def validate_components(components):
    """
    Validates the given components.
    
    Parameters
    ----------
    components : `None | iterable` of `instance<Component>`
        The components to validate.
    
    Returns
    -------
    components_processed : `None | tuple<Component>`
    
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
        
        if not component.type.layout_flags.nestable:
            raise ValueError(
                f'Cannot nest components of type {component.type.name}, '
                f'got {component!r}; components = {components!r}.'
            )
        
        if (components_processed is None):
            components_processed = []
        
        components_processed.append(component)
    
    if (components_processed is not None):
        components_processed = tuple(components_processed)
    
    return components_processed


# custom_id

parse_custom_id = nullable_string_parser_factory('custom_id')
put_custom_id_into = url_optional_putter_factory('custom_id')
validate_custom_id = nullable_string_validator_factory('custom_id', 0, CUSTOM_ID_LENGTH_MAX)

# emoji

parse_emoji = nullable_functional_parser_factory('emoji', create_partial_emoji_from_data)
put_emoji_into = nullable_functional_optional_putter_factory('emoji', create_partial_emoji_data)
validate_emoji = nullable_entity_validator_factory('emoji', Emoji)
