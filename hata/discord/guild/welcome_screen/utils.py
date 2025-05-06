__all__ = ()

from .fields import (
    put_description, put_enabled, put_welcome_channels, validate_description, validate_enabled,
    validate_welcome_channels
)


WELCOME_SCREEN_FIELD_CONVERTERS = {
    'description': (validate_description, put_description),
    'enabled': (validate_enabled, put_enabled),
    'welcome_channels': (validate_welcome_channels, put_welcome_channels),
}
