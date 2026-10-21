__all__ = ()

from ...fields.field_parsers import nullable_object_array_parser_factory
from ...fields.field_putters import force_bool_putter_factory, nullable_object_array_optional_putter_factory
from ...fields.field_validators import (
    bool_validator_factory, nullable_object_array_validator_factory, nullable_string_validator_factory
)
from ...fields.fields_common import parse_description, put_description

from ..welcome_screen_channel import WelcomeScreenChannel

from .constants import DESCRIPTION_LENGTH_MAX

# description

validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)

# enabled

put_enabled = force_bool_putter_factory('enabled')
validate_enabled = bool_validator_factory('enabled', True)

# welcome_channels

parse_welcome_channels = nullable_object_array_parser_factory('welcome_channels', WelcomeScreenChannel)
put_welcome_channels = nullable_object_array_optional_putter_factory('welcome_channels')
validate_welcome_channels = nullable_object_array_validator_factory('welcome_channels', WelcomeScreenChannel)
