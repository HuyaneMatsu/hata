__all__ = ()

from ...field_parsers import bool_parser_factory, force_string_parser_factory, nullable_string_parser_factory
from ...field_putters import (
    bool_optional_putter_factory, nullable_string_optional_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, nullable_string_validator_factory, url_required_validator_factory
)

from .constants import DESCRIPTION_LENGTH_MIN, DESCRIPTION_LENGTH_MAX


# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_optional_putter_factory('description')
validate_description = nullable_string_validator_factory(
    'description', DESCRIPTION_LENGTH_MIN, DESCRIPTION_LENGTH_MAX
)


# spoiler

parse_spoiler = bool_parser_factory('spoiler', False)
put_spoiler_into = bool_optional_putter_factory('spoiler', False)
validate_spoiler = bool_validator_factory('spoiler', False)


# url

parse_url = force_string_parser_factory('url')
put_url_into = url_optional_putter_factory('url')
validate_url = url_required_validator_factory('url')
