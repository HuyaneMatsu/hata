__all__ = ()

from .fields import (
    put_description_into, put_enabled_into, put_welcome_channels_into, validate_description, validate_enabled,
    validate_welcome_channels
)


WELCOME_SCREEN_FIELD_CONVERTERS = {
    'description': (validate_description, put_description_into),
    'enabled': (validate_enabled, put_enabled_into),
    'welcome_channels': (validate_welcome_channels, put_welcome_channels_into),
}
