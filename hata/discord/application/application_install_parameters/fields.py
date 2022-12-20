__all__ = ()

from ...field_parsers import flag_parser_factory, preinstanced_array_parser_factory
from ...field_putters import preinstanced_array_putter_factory, string_flag_putter_factory
from ...field_validators import flag_validator_factory, preinstanced_array_validator_factory
from ...oauth2 import Oauth2Scope
from ...permission import Permission
from ...permission.constants import PERMISSION_KEY

# permissions

parse_permissions = flag_parser_factory(PERMISSION_KEY, Permission)
put_permissions_into = string_flag_putter_factory(PERMISSION_KEY)
validate_permissions = flag_validator_factory(PERMISSION_KEY, Permission)

# scopes

parse_scopes = preinstanced_array_parser_factory('scopes', Oauth2Scope)
put_scopes_into = preinstanced_array_putter_factory('scopes')
validate_scopes = preinstanced_array_validator_factory('scopes', Oauth2Scope)
