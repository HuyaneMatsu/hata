__all__ = ()

from ...field_parsers import bool_parser_factory, force_string_parser_factory, nullable_string_parser_factory
from ...field_putters import bool_optional_putter_factory, force_string_putter_factory, nullable_string_putter_factory
from ...field_validators import (
    bool_validator_factory, force_string_validator_factory, nullable_string_validator_factory
)

from .constants import DESCRIPTION_LENGTH_MAX, LABEL_LENGTH_MAX, VALUE_LENGTH_MAX


# default

parse_default = bool_parser_factory('default', False)
put_default_into = bool_optional_putter_factory('default', False)
validate_default = bool_validator_factory('default', False)

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)

# label

parse_label = force_string_parser_factory('label')
put_label_into = force_string_putter_factory('label')
validate_label = nullable_string_validator_factory('label', 0, LABEL_LENGTH_MAX)

# value

parse_value = force_string_parser_factory('value')
put_value_into = force_string_putter_factory('value')
validate_value = force_string_validator_factory('value', 0, VALUE_LENGTH_MAX)
