__all__ = ()

from ...field_parsers import nullable_object_array_parser_factory, nullable_string_parser_factory
from ...field_putters import (
    force_bool_putter_factory, nullable_object_array_optional_putter_factory, nullable_string_putter_factory
)
from ...field_validators import (
    bool_validator_factory, nullable_object_array_validator_factory, nullable_string_validator_factory
)

from ..welcome_screen_channel import WelcomeScreenChannel

from .constants import DESCRIPTION_LENGTH_MAX

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)

# enabled

put_enabled_into = force_bool_putter_factory('enabled')
validate_enabled = bool_validator_factory('enabled', True)

# welcome_channels

parse_welcome_channels = nullable_object_array_parser_factory('welcome_channels', WelcomeScreenChannel)
put_welcome_channels_into = nullable_object_array_optional_putter_factory('welcome_channels')
validate_welcome_channels = nullable_object_array_validator_factory('welcome_channels', WelcomeScreenChannel)
