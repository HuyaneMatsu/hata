__all__ = ()

from ...channel import Channel
from ...field_parsers import (
    default_entity_parser_factory, entity_id_parser_factory, nullable_string_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_optional_putter_factory, entity_putter_factory, nullable_string_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    default_entity_validator, entity_id_validator_factory, nullable_string_validator_factory,
    preinstanced_validator_factory
)
from ...message import Message
from ...user import ClientUserBase

from ..action import AutoModerationAction
from ..rule import AutoModerationRule, AutoModerationRuleTriggerType

# action

parse_action = default_entity_parser_factory('action', AutoModerationAction, AutoModerationAction())
put_action_into = entity_putter_factory('action', AutoModerationAction)
validate_action = default_entity_validator('action', AutoModerationAction, AutoModerationAction())

# alert_system_message_id

parse_alert_system_message_id = entity_id_parser_factory('alert_system_message_id')
put_alert_system_message_id_into = entity_id_optional_putter_factory('alert_system_message_id')
validate_alert_system_message_id = entity_id_validator_factory('alert_system_message_id', Message)

# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_optional_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', Channel)

# content

parse_content = nullable_string_parser_factory('content')
put_content_into = nullable_string_putter_factory('content')
validate_content = nullable_string_validator_factory('content', 0, 10000)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', include = 'Guild')

# matched_content

parse_matched_content = nullable_string_parser_factory('matched_content')
put_matched_content_into = nullable_string_putter_factory('matched_content')
validate_matched_content = nullable_string_validator_factory('matched_content', 0, 10000)

# matched_keyword

parse_matched_keyword = nullable_string_parser_factory('matched_keyword')
put_matched_keyword_into = nullable_string_putter_factory('matched_keyword')
validate_matched_keyword = nullable_string_validator_factory('matched_keyword', 0, 10000)

# rule_id

parse_rule_id = entity_id_parser_factory('rule_id')
put_rule_id_into = entity_id_optional_putter_factory('rule_id')
validate_rule_id = entity_id_validator_factory('rule_id', AutoModerationRule)

# rule_trigger_type

parse_rule_trigger_type = preinstanced_parser_factory(
    'rule_trigger_type', AutoModerationRuleTriggerType, AutoModerationRuleTriggerType.none
)
put_rule_trigger_type_into = preinstanced_putter_factory('rule_trigger_type')
validate_rule_trigger_type = preinstanced_validator_factory('rule_trigger_type', AutoModerationRuleTriggerType)

# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id_into = entity_id_optional_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
