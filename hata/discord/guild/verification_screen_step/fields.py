__all__ = ()

from ...fields.field_parsers import nullable_array_parser_factory, preinstanced_parser_factory
from ...fields.field_putters import nullable_string_array_optional_putter_factory, preinstanced_putter_factory
from ...fields.field_validators import (
    force_string_validator_factory, nullable_string_array_validator_factory, preinstanced_validator_factory
)
from ...fields.fields_common import (
    parse_required, parse_title__from_label as parse_title, put_required__optional as put_required,
    put_title__to_label as put_title, validate_required
)

from .constants import TITLE_LENGTH_MAX
from .preinstanced import VerificationScreenStepType


# title

validate_title = force_string_validator_factory('title', 0, TITLE_LENGTH_MAX)

# type

parse_type = preinstanced_parser_factory('field_type', VerificationScreenStepType, VerificationScreenStepType.none)
put_type = preinstanced_putter_factory('field_type')
validate_type = preinstanced_validator_factory('type', VerificationScreenStepType)

# values

parse_values = nullable_array_parser_factory('values')
put_values = nullable_string_array_optional_putter_factory('values')
validate_values = nullable_string_array_validator_factory('values')
