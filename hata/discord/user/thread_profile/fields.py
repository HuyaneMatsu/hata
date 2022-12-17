__all__ = ()

from ...field_parsers import flag_parser_factory, nullable_date_time_parser_factory
from ...field_putters import flag_optional_putter_factory, nullable_date_time_optional_putter_factory
from ...field_validators import flag_validator_factory, nullable_date_time_validator_factory

from .flags import ThreadProfileFlag

# flags

parse_flags = flag_parser_factory('flags', ThreadProfileFlag)
put_flags_into = flag_optional_putter_factory('flags', ThreadProfileFlag())
validate_flags = flag_validator_factory('flags', ThreadProfileFlag)

# joined_at

parse_joined_at = nullable_date_time_parser_factory('joined_at')
put_joined_at_into = nullable_date_time_optional_putter_factory('joined_at')
validate_joined_at = nullable_date_time_validator_factory('joined_at')
