__all__ = ()

from ...field_parsers import entity_id_parser_factory
from ...field_putters import entity_id_putter_factory
from ...field_validators import entity_id_validator_factory
from ...user import ClientUserBase

from ..guild import Guild

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id_into = entity_id_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
