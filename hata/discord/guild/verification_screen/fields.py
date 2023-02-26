__all__ = ()

from ...field_parsers import (
    nullable_date_time_parser_factory, nullable_object_array_parser_factory, nullable_string_parser_factory
)
from ...field_putters import (
    force_bool_putter_factory, nullable_date_time_optional_putter_factory,
    nullable_object_array_optional_putter_factory, nullable_string_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, nullable_date_time_validator_factory, nullable_object_array_validator_factory,
    nullable_string_validator_factory
)

from ..verification_screen_step import VerificationScreenStep

from .constants import DESCRIPTION_LENGTH_MAX

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_optional_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)

# edited_at

parse_edited_at = nullable_date_time_parser_factory('version')
put_edited_at_into = nullable_date_time_optional_putter_factory('version')
validate_edited_at = nullable_date_time_validator_factory('edited_at')

# enabled

put_enabled_into = force_bool_putter_factory('enabled')
validate_enabled = bool_validator_factory('enabled', True)

# steps

parse_steps = nullable_object_array_parser_factory('form_fields', VerificationScreenStep)
put_steps_into = nullable_object_array_optional_putter_factory('form_fields')
validate_steps = nullable_object_array_validator_factory('steps', VerificationScreenStep)
