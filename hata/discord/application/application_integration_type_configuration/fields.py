__all__ = ()

from ...fields.field_parsers import nullable_entity_parser_factory
from ...fields.field_putters import nullable_entity_optional_putter_factory
from ...fields.field_validators import nullable_entity_validator_factory

from ..application_install_parameters import ApplicationInstallParameters

# install_parameters

parse_install_parameters = nullable_entity_parser_factory('oauth2_install_params', ApplicationInstallParameters)
put_install_parameters = nullable_entity_optional_putter_factory(
    'oauth2_install_params', ApplicationInstallParameters
)
validate_install_parameters = nullable_entity_validator_factory('install_parameters', ApplicationInstallParameters)
