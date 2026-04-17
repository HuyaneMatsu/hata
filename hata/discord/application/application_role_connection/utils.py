__all__ = ()

from .fields import (
    put_metadata_values, put_platform_name, put_platform_user_name, validate_metadata_values,
    validate_platform_name, validate_platform_user_name
)


APPLICATION_ROLE_CONNECTION_FIELD_CONVERTERS = {
    'platform_name': (validate_platform_name, put_platform_name),
    'platform_user_name': (validate_platform_user_name, put_platform_user_name),
    'metadata_values': (validate_metadata_values, put_metadata_values),
}

