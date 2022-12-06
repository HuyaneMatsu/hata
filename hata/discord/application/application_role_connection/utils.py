__all__ = ()

from .fields import (
    put_metadata_values_into, put_platform_name_into, put_platform_user_name_into, validate_metadata_values,
    validate_platform_name, validate_platform_user_name
)


APPLICATION_ROLE_CONNECTION_FIELD_CONVERTERS = {
    'platform_name': (validate_platform_name, put_platform_name_into),
    'platform_user_name': (validate_platform_user_name, put_platform_user_name_into),
    'metadata_values': (validate_metadata_values, put_metadata_values_into),
}

