__all__ = ()

from ..scheduled_event import ScheduledEvent

from ...field_parsers import entity_id_parser_factory
from ...field_putters import entity_id_putter_factory
from ...field_validators import entity_id_validator_factory
from ...user import ClientUserBase

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# scheduled_event_id

parse_scheduled_event_id = entity_id_parser_factory('guild_scheduled_event_id')
put_scheduled_event_id_into = entity_id_putter_factory('guild_scheduled_event_id')
validate_scheduled_event_id = entity_id_validator_factory('scheduled_event_id', ScheduledEvent)

# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id_into = entity_id_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
