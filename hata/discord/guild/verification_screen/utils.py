__all__ = ()

from .fields import (
    put_description, put_enabled, put_steps, validate_description, validate_enabled, validate_steps
)


VERIFICATION_SCREEN_FIELD_CONVERTERS = {
    'description': (validate_description, put_description),
    'enabled': (validate_enabled, put_enabled),
    'steps': (validate_steps, put_steps),
}
