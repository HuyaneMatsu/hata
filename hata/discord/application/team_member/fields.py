__all__ = ()

from ...field_parsers import default_entity_parser_factory, preinstanced_parser_factory
from ...field_putters import default_entity_putter_factory, preinstanced_putter_factory
from ...field_validators import default_entity_validator_factory, preinstanced_validator_factory
from ...user import ClientUserBase, User, ZEROUSER

from .preinstanced import TeamMemberRole, TeamMembershipState

# role

parse_role = preinstanced_parser_factory('role', TeamMemberRole, TeamMemberRole.none)
put_role = preinstanced_putter_factory('role')
validate_role = preinstanced_validator_factory('role', TeamMemberRole)

# state

parse_state = preinstanced_parser_factory('membership_state', TeamMembershipState, TeamMembershipState.none)
put_state = preinstanced_putter_factory('membership_state')
validate_state = preinstanced_validator_factory('state', TeamMembershipState)

# user

parse_user = default_entity_parser_factory('user', User, default = ZEROUSER)
put_user = default_entity_putter_factory('user', ClientUserBase, ZEROUSER, force_include_internals = True)
validate_user = default_entity_validator_factory('user', ClientUserBase, default = ZEROUSER)
