__all__ = ()

from ...field_parsers import (
    bool_parser_factory, int_parser_factory, nullable_array_parser_factory, preinstanced_array_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, int_putter_factory, nullable_string_array_optional_putter_factory,
    preinstanced_array_putter_factory
)
from ...field_validators import (
    bool_validator_factory, int_conditional_validator_factory, nullable_string_array_validator_factory,
    preinstanced_array_validator_factory
)

from .constants import AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
from .preinstanced import AutoModerationKeywordPresetType

# excluded_keywords

parse_excluded_keywords = nullable_array_parser_factory('allow_list')
put_excluded_keywords_into = nullable_string_array_optional_putter_factory('allow_list')
validate_excluded_keywords = nullable_string_array_validator_factory('excluded_keywords')

# keyword_presets

parse_keyword_presets = preinstanced_array_parser_factory('presets', AutoModerationKeywordPresetType)
put_keyword_presets_into = preinstanced_array_putter_factory('presets')
validate_keyword_presets = preinstanced_array_validator_factory('keyword_presets', AutoModerationKeywordPresetType)

# keywords

parse_keywords = nullable_array_parser_factory('keyword_filter')
put_keywords_into = nullable_string_array_optional_putter_factory('keyword_filter')
validate_keywords = nullable_string_array_validator_factory('keywords')

# mention_limit

parse_mention_limit = int_parser_factory('mention_total_limit', AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX)
put_mention_limit_into = int_putter_factory('mention_total_limit')
validate_mention_limit = int_conditional_validator_factory(
    'mention_limit',
    AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX,
    (
        lambda mention_limit:
        mention_limit >= 0 and mention_limit <= AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
    ),
    f'>= {0} and <= {AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX},'
)

# raid_protection

parse_raid_protection = bool_parser_factory('mention_raid_protection_enabled', False)
put_raid_protection_into = bool_optional_putter_factory('mention_raid_protection_enabled', False)
validate_raid_protection = bool_validator_factory('raid_protection', False)

# regex_patterns

parse_regex_patterns = nullable_array_parser_factory('regex_patterns')
put_regex_patterns_into = nullable_string_array_optional_putter_factory('regex_patterns')
validate_regex_patterns = nullable_string_array_validator_factory('regex_patterns')
