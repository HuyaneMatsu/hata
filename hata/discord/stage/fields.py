__all__ = ()

from ..channel import Channel
from ..field_parsers import (
    bool_parser_factory, entity_id_parser_factory, negated_bool_parser_factory, nullable_string_parser_factory,
    preinstanced_parser_factory
)
from ..field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    negated_bool_optional_putter_factory, nullable_string_putter_factory, preinstanced_putter_factory,
    url_optional_putter_factory
)
from ..field_validators import (
    bool_validator_factory, entity_id_validator_factory, nullable_string_validator_factory,
    preinstanced_validator_factory
)
from ..scheduled_event import PrivacyLevel
from ..scheduled_event import ScheduledEvent

from .constants import TOPIC_LENGTH_MAX, TOPIC_LENGTH_MIN


# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', Channel)

# discoverable

parse_discoverable = negated_bool_parser_factory('discoverable_disabled', True)
put_discoverable_into = negated_bool_optional_putter_factory('discoverable_disabled', True)
validate_discoverable = bool_validator_factory('discoverable', True)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('emoji_id')

# invite_code

parse_invite_code = nullable_string_parser_factory('invite_code')
put_invite_code_into = url_optional_putter_factory('invite_code')
validate_invite_code = nullable_string_validator_factory('invite_code', 0, 1024)

# privacy_level

parse_privacy_level = preinstanced_parser_factory('privacy_level', PrivacyLevel, PrivacyLevel.guild_only)
put_privacy_level_into = preinstanced_putter_factory('privacy_level')
validate_privacy_level = preinstanced_validator_factory('privacy_level', PrivacyLevel)

# scheduled_event_id

parse_scheduled_event_id = entity_id_parser_factory('guild_scheduled_event_id')
put_scheduled_event_id_into = entity_id_optional_putter_factory('guild_scheduled_event_id')
validate_scheduled_event_id = entity_id_validator_factory('scheduled_event_id', ScheduledEvent)

# send_start_notification

parse_send_start_notification = bool_parser_factory('send_start_notification', False)
put_send_start_notification_into = bool_optional_putter_factory('send_start_notification', False)
validate_send_start_notification = bool_validator_factory('send_start_notification', False)

# topic

parse_topic = nullable_string_parser_factory('topic')
put_topic_into = nullable_string_putter_factory('topic')
validate_topic = nullable_string_validator_factory('topic', TOPIC_LENGTH_MIN, TOPIC_LENGTH_MAX)
