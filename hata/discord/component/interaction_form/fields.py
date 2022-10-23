__all__ = ()

from ...field_parsers import nullable_string_parser_factory
from ...field_putters import nullable_string_optional_putter_factory
from ...field_validators import nullable_string_validator_factory

from ..shared_fields import validate_components as validate_any_components

from ..component import Component, ComponentType

from .constants import TITLE_LENGTH_MIN, TITLE_LENGTH_MAX

# components

def validate_components(components):
    """
    Interaction form specific component validator.
    
    Parameters
    ----------
    components : `None`, `iterable` of ``Component``
        The components to validate.
    
    Returns
    -------
    components : `None`, `tuple` of ``Component``
    """
    components = validate_any_components(components)
    if (components is not None):
        return tuple(
            component if (component.type is ComponentType.row)
            else Component(ComponentType.row, components = [component])
            for component in components
        )

# title

parse_title = nullable_string_parser_factory('title')
put_title_into = nullable_string_optional_putter_factory('title')
validate_title = nullable_string_validator_factory('title', TITLE_LENGTH_MIN, TITLE_LENGTH_MAX)
