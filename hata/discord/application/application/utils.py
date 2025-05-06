__all__ = ()

from functools import partial as partial_func

from .application import APPLICATION_COVER, APPLICATION_ICON
from .fields import (
    put_custom_install_url, put_description, put_flags, put_install_parameters,
    put_interaction_endpoint_url, put_role_connection_verification_url, put_tags,
    validate_custom_install_url, validate_description, validate_flags, validate_install_parameters,
    validate_interaction_endpoint_url, validate_role_connection_verification_url, validate_tags
)


APPLICATION_FIELD_CONVERTERS = {
    'cover': (
        partial_func(APPLICATION_COVER.validate_icon, allow_data = True),
        partial_func(APPLICATION_COVER.put_into, as_data = True),
    ),
    'custom_install_url': (validate_custom_install_url, put_custom_install_url),
    'description': (validate_description, put_description),
    'flags': (validate_flags, put_flags),
    'icon': (
        partial_func(APPLICATION_ICON.validate_icon, allow_data = True),
        partial_func(APPLICATION_ICON.put_into, as_data = True),
    ),
    'install_parameters': (validate_install_parameters, put_install_parameters),
    'interaction_endpoint_url': (validate_interaction_endpoint_url, put_interaction_endpoint_url),
    'role_connection_verification_url': (
        validate_role_connection_verification_url, put_role_connection_verification_url,
    ),
    'tags': (validate_tags, put_tags),
}
