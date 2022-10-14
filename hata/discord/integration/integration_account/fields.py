__all__ = ()

from ...field_parsers import force_string_parser_factory
from ...field_putters import force_string_putter_factory
from ...field_validators import force_string_validator_factory

from .constants import ID_LENGTH_MAX, ID_LENGTH_MIN, NAME_LENGTH_MAX, NAME_LENGTH_MIN

# id

parse_id = force_string_parser_factory('id')
put_id_into = force_string_putter_factory('id')
validate_id = force_string_validator_factory('integration_account_id', ID_LENGTH_MIN, ID_LENGTH_MAX)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)
