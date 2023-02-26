__all__ = ()

from ...field_parsers import (
    bool_parser_factory, nullable_date_time_parser_factory, nullable_sorted_array_parser_factory,
    preinstanced_array_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, nullable_date_time_optional_putter_factory,
    nullable_string_array_optional_putter_factory, preinstanced_array_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, nullable_date_time_validator_factory, nullable_string_array_validator_factory,
    preinstanced_array_validator_factory, preinstanced_validator_factory
)

from ..discovery_category import DiscoveryCategory

# application_actioned

parse_application_actioned = nullable_date_time_parser_factory('partner_actioned_timestamp')
put_application_actioned_into = nullable_date_time_optional_putter_factory('partner_actioned_timestamp')
validate_application_actioned = nullable_date_time_validator_factory('application_actioned')

# application_requested

parse_application_requested = nullable_date_time_parser_factory('partner_application_timestamp')
put_application_requested_into = nullable_date_time_optional_putter_factory('partner_application_timestamp')
validate_application_requested = nullable_date_time_validator_factory('application_requested')

# emoji_discovery

parse_emoji_discovery = bool_parser_factory('emoji_discoverability_enabled', False)
put_emoji_discovery_into = bool_optional_putter_factory('emoji_discoverability_enabled', False)
validate_emoji_discovery = bool_validator_factory('emoji_discovery', False)

# keywords

parse_keywords = nullable_sorted_array_parser_factory('keywords')
put_keywords_into = nullable_string_array_optional_putter_factory('keywords')
validate_keywords = nullable_string_array_validator_factory('keywords')

# primary_category

parse_primary_category = preinstanced_parser_factory(
    'primary_category_id', DiscoveryCategory, DiscoveryCategory.general
)
put_primary_category_into = preinstanced_putter_factory('primary_category_id')
validate_primary_category = preinstanced_validator_factory('primary_category', DiscoveryCategory)

# sub_categories

parse_sub_categories = preinstanced_array_parser_factory('category_ids', DiscoveryCategory)
put_sub_categories_into = preinstanced_array_putter_factory('category_ids')
validate_sub_categories = preinstanced_array_validator_factory('sub_categories', DiscoveryCategory)
