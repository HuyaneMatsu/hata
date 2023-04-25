__all__ = ()

from ...field_parsers import (
    default_entity_parser_factory, preinstanced_array_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    default_entity_putter_factory, preinstanced_array_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    default_entity_validator, preinstanced_array_validator_factory, preinstanced_validator_factory
)
from ...user import ClientUserBase, User, ZEROUSER

from .preinstanced import TeamMemberPermission, TeamMembershipState

# permissions

parse_permissions = preinstanced_array_parser_factory('permissions', TeamMemberPermission)
put_permissions_into = preinstanced_array_putter_factory('permissions')
validate_permissions = preinstanced_array_validator_factory('permissions', TeamMemberPermission)

# state

parse_state = preinstanced_parser_factory('membership_state', TeamMembershipState, TeamMembershipState.none)
put_state_into = preinstanced_putter_factory('membership_state')
validate_state = preinstanced_validator_factory('state', TeamMembershipState)

# user

parse_user = default_entity_parser_factory('user', User, default = ZEROUSER)
put_user_into = default_entity_putter_factory('user', ClientUserBase, ZEROUSER)
validate_user = default_entity_validator('user', ClientUserBase, default = ZEROUSER)
