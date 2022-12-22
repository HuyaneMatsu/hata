__all__ = ()

from .fields import (
    put_description_into, put_enabled_into, put_steps_into, validate_description, validate_enabled, validate_steps
)


VERIFICATION_SCREEN_FIELD_CONVERTERS = {
    'description': (validate_description, put_description_into),
    'enabled': (validate_enabled, put_enabled_into),
    'steps': (validate_steps, put_steps_into),
}
