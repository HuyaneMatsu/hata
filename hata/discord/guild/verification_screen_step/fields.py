__all__ = ()

from ...field_parsers import (
    bool_parser_factory, force_string_parser_factory, nullable_sorted_array_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, force_string_putter_factory, nullable_string_array_optional_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, force_string_validator_factory, nullable_string_array_validator_factory,
    preinstanced_validator_factory
)

from .constants import TITLE_LENGTH_MAX
from .preinstanced import VerificationScreenStepType

# required

parse_required = bool_parser_factory('required', False)
put_required_into = bool_optional_putter_factory('required', False)
validate_required = bool_validator_factory('required', False)

# title

parse_title = force_string_parser_factory('label')
put_title_into = force_string_putter_factory('label')
validate_title = force_string_validator_factory('title', 0, TITLE_LENGTH_MAX)

# type

parse_type = preinstanced_parser_factory('field_type', VerificationScreenStepType, VerificationScreenStepType.none)
put_type_into = preinstanced_putter_factory('field_type')
validate_type = preinstanced_validator_factory('type', VerificationScreenStepType)

# values

parse_values = nullable_sorted_array_parser_factory('values')
put_values_into = nullable_string_array_optional_putter_factory('values')
validate_values = nullable_string_array_validator_factory('values')
