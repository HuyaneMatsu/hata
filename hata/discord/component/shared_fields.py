__all__ = ()

from scarletio import include

from ..emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data
from ..field_parsers import nullable_functional_parser_factory, nullable_string_parser_factory
from ..field_putters import nullable_functional_optional_putter_factory, url_optional_putter_factory
from ..field_validators import nullable_entity_validator_factory, nullable_string_validator_factory

from .shared_constants import CUSTOM_ID_LENGTH_MAX

Component = include('Component')

# components

def parse_components(data):
    """
    Parses out components from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Components data.
    
    Returns
    -------
    components : `None`, `tuple` of ``Component``
    """
    component_datas = data.get('components', None)
    if (component_datas is not None) and component_datas:
        return tuple(Component.from_data(component_data) for component_data in component_datas)


def put_components_into(components, data, defaults):
    """
    Puts the given components to the given `data`.
    
    Parameters
    ----------
    components : `None`, `tuple` of ``Component``
        The components to serialize.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default fields should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if (components is None):
        component_datas = []
    else:
        component_datas = [component.to_data(defaults = defaults) for component in components]
    data['components'] = component_datas
    
    return data


def validate_components(components):
    """
    Validates the `components` field of ``Component``.
    
    Parameters
    ----------
    components : `None` or `iterable` of ``Component``
        Sub-components.
    
    Returns
    -------
    components : `None`, `tuple` of ``Component``
    
    Raises
    ------
    TypeError
        - If `components` is not iterable.
        - If `components contains a non ``Component`` element.
    ValueError
        - If `component`'s length is out of the expected range.
    """
    if (components is None):
        return None
    
    if (getattr(components, '__iter__', None) is None):
        raise TypeError(
            f'`components` can `None` or `iterable`, got {components.__class__.__name__}; {components!r}.'
        )
    
    components_processed = None
    
    for component in components:
        if not isinstance(component, Component):
            raise TypeError(
                f'`components` elements can be `{Component.__name__}` instances, got '
                f'{component.__class__.__name__}; {component!r}; components={components}.'
            )
        
        if (components_processed is None):
            components_processed = []
        
        components_processed.append(component)
    
    if (components_processed is not None):
        return tuple(components_processed)

# custom_id

parse_custom_id = nullable_string_parser_factory('custom_id')
put_custom_id_into = url_optional_putter_factory('custom_id')
validate_custom_id = nullable_string_validator_factory('custom_id', 0, CUSTOM_ID_LENGTH_MAX)

# emoji

parse_emoji = nullable_functional_parser_factory('emoji', create_partial_emoji_from_data)
put_emoji_into = nullable_functional_optional_putter_factory('emoji', create_partial_emoji_data)
validate_emoji = nullable_entity_validator_factory('emoji', Emoji)
