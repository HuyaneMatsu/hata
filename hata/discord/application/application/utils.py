__all__ = ()

from functools import partial as partial_func

from .application import APPLICATION_COVER, APPLICATION_ICON
from .fields import (
    put_custom_install_url_into, put_description_into, put_flags_into, put_install_parameters_into,
    put_interaction_endpoint_url_into, put_role_connection_verification_url_into, put_tags_into,
    validate_custom_install_url, validate_description, validate_flags, validate_install_parameters,
    validate_interaction_endpoint_url, validate_role_connection_verification_url, validate_tags
)


APPLICATION_FIELD_CONVERTERS = {
    'cover': (
        partial_func(APPLICATION_COVER.validate_icon, allow_data = True),
        partial_func(APPLICATION_COVER.put_into, as_data = True),
    ),
    'custom_install_url': (validate_custom_install_url, put_custom_install_url_into),
    'description': (validate_description, put_description_into),
    'flags': (validate_flags, put_flags_into),
    'icon': (
        partial_func(APPLICATION_ICON.validate_icon, allow_data = True),
        partial_func(APPLICATION_ICON.put_into, as_data = True),
    ),
    'install_parameters': (validate_install_parameters, put_install_parameters_into),
    'interaction_endpoint_url': (validate_interaction_endpoint_url, put_interaction_endpoint_url_into),
    'role_connection_verification_url': (
        validate_role_connection_verification_url, put_role_connection_verification_url_into,
    ),
    'tags': (validate_tags, put_tags_into),
}
