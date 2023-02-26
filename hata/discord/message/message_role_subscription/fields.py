__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, force_string_parser_factory, int_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, force_string_putter_factory, int_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, force_string_validator_factory,
    int_conditional_validator_factory
)


# renewal

parse_renewal = bool_parser_factory('is_renewal', False)
put_renewal_into = bool_optional_putter_factory('is_renewal', False)
validate_renewal = bool_validator_factory('renewal', False)

# subscription_listing_id

parse_subscription_listing_id = entity_id_parser_factory('role_subscription_listing_id')
put_subscription_listing_id_into = entity_id_optional_putter_factory('role_subscription_listing_id')
validate_subscription_listing_id = entity_id_validator_factory('subscription_listing_id')

# tier_name

parse_tier_name = force_string_parser_factory('tier_name')
put_tier_name_into = force_string_putter_factory('tier_name')
validate_tier_name = force_string_validator_factory('tier_name', 0, 1024)

# total_months

parse_total_months = int_parser_factory('total_months_subscribed', 1)
put_total_months_into = int_putter_factory('total_months_subscribed')
validate_total_months = int_conditional_validator_factory(
    'total_months',
    1,
    lambda total_months : total_months >= 1,
    '>= 1',
)
