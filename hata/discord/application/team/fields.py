__all__ = ()

from ...field_parsers import (
    entity_id_parser_factory, force_string_parser_factory, nullable_entity_array_parser_factory
)
from ...field_putters import (
    entity_id_putter_factory, force_string_putter_factory, nullable_entity_array_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, force_string_validator_factory, nullable_entity_array_validator_factory
)
from ...user import ClientUserBase

from ..team_member import TeamMember

from .constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('team_id')

# members

parse_members = nullable_entity_array_parser_factory('members', TeamMember)
put_members_into = nullable_entity_array_putter_factory('members', TeamMember)
validate_members = nullable_entity_array_validator_factory('members', TeamMember)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# owner_id

parse_owner_id = entity_id_parser_factory('owner_user_id')
put_owner_id_into = entity_id_putter_factory('owner_user_id')
validate_owner_id = entity_id_validator_factory('owner_id', ClientUserBase)
