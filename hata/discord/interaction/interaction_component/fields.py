__all__ = ()

from ...component import ComponentType
from ...component.shared_constants import CUSTOM_ID_LENGTH_MAX
from ...field_parsers import (
    field_parser_factory, nullable_object_array_parser_factory, nullable_string_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    nullable_field_optional_putter_factory, nullable_object_array_optional_putter_factory, preinstanced_putter_factory,
    url_optional_putter_factory
)
from ...field_validators import (
    field_validator_factory, nullable_object_array_validator_factory, nullable_string_validator_factory,
    preinstanced_validator_factory
)

# components

parse_components = nullable_object_array_parser_factory('components', NotImplemented, include = 'InteractionComponent')
put_components_into = nullable_object_array_optional_putter_factory('components')
validate_components = nullable_object_array_validator_factory(
    'components', NotImplemented, include = 'InteractionComponent'
)

# custom_id

parse_custom_id = nullable_string_parser_factory('custom_id')
put_custom_id_into = url_optional_putter_factory('custom_id')
validate_custom_id = nullable_string_validator_factory('custom_id', 0, CUSTOM_ID_LENGTH_MAX)

# type

parse_type = preinstanced_parser_factory('type', ComponentType, ComponentType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', ComponentType)

# value

parse_value = field_parser_factory('value')
put_value_into = nullable_field_optional_putter_factory('value')
validate_value = field_validator_factory('value')
