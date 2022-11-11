__all__ = ()

from ...field_parsers import (
    bool_parser_factory, field_parser_factory, force_string_parser_factory, nullable_object_array_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, force_string_putter_factory, nullable_field_optional_putter_factory,
    nullable_object_array_optional_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, field_validator_factory, force_string_validator_factory,
    nullable_object_array_validator_factory, preinstanced_validator_factory
)

from ...application_command import ApplicationCommandOptionType
from ...application_command.constants import APPLICATION_COMMAND_NAME_LENGTH_MAX, APPLICATION_COMMAND_NAME_LENGTH_MIN

# focused

parse_focused = bool_parser_factory('focused', False)
put_focused_into = bool_optional_putter_factory('focused', False)
validate_focused = bool_validator_factory('focused')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory(
    'name', APPLICATION_COMMAND_NAME_LENGTH_MIN, APPLICATION_COMMAND_NAME_LENGTH_MAX
)

# options

parse_options = nullable_object_array_parser_factory('options', NotImplemented, include = 'InteractionOption')
put_options_into = nullable_object_array_optional_putter_factory('options')
validate_options = nullable_object_array_validator_factory('options', NotImplemented, include = 'InteractionOption')

# type

parse_type = preinstanced_parser_factory('type', ApplicationCommandOptionType, ApplicationCommandOptionType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', ApplicationCommandOptionType)

# value

parse_value = field_parser_factory('value')
put_value_into = nullable_field_optional_putter_factory('value')
validate_value = field_validator_factory('value')
