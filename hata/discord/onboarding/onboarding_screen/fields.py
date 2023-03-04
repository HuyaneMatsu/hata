__all__ = ()

from ...field_parsers import entity_id_parser_factory, nullable_object_array_parser_factory, bool_parser_factory, \
    entity_id_array_parser_factory
from ...field_putters import entity_id_putter_factory, nullable_entity_array_putter_factory, \
    bool_optional_putter_factory, entity_id_array_optional_putter_factory
from ...field_validators import entity_id_validator_factory, nullable_object_array_validator_factory, \
    bool_validator_factory, entity_id_array_validator_factory
from ...guild import Guild
from ..onboarding_prompt import OnboardingPrompt
from ...channel import Channel

# default_channel_ids

parse_default_channel_ids = entity_id_array_parser_factory('default_channel_ids')
put_default_channel_ids_into = entity_id_array_optional_putter_factory('default_channel_ids')
validate_default_channel_ids = entity_id_array_validator_factory('default_channel_ids', Channel)

# enabled

parse_enabled = bool_parser_factory('enabled', True)
put_enabled_into = bool_optional_putter_factory('enabled', True)
validate_enabled = bool_validator_factory('enabled', True)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# prompts

parse_prompts = nullable_object_array_parser_factory('prompts', OnboardingPrompt)
put_prompts_into = nullable_entity_array_putter_factory('prompts', OnboardingPrompt)
validate_prompts = nullable_object_array_validator_factory('prompts', OnboardingPrompt)
