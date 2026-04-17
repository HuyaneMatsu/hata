__all__ = ()


from ...field_parsers import (
    entity_id_array_parser_factory, entity_id_parser_factory, nullable_date_time_parser_factory,
    nullable_string_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_putter_factory, nullable_date_time_optional_putter_factory,
    optional_entity_id_array_optional_putter_factory, preinstanced_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    entity_id_array_validator_factory, entity_id_validator_factory, nullable_date_time_validator_factory,
    nullable_string_validator_factory, preinstanced_validator_factory
)
from ...user import ClientUserBase

from ..sku import SKU

from .preinstanced import SubscriptionStatus


# cancelled_at

parse_cancelled_at = nullable_date_time_parser_factory('cancelled_at')
put_cancelled_at = nullable_date_time_optional_putter_factory('cancelled_at')
validate_cancelled_at = nullable_date_time_validator_factory('cancelled_at')


# country_code

parse_country_code = nullable_string_parser_factory('country')
put_country_code = url_optional_putter_factory('country')
validate_country_code = nullable_string_validator_factory('country_code', 2, 2)


# current_period_end

parse_current_period_end = nullable_date_time_parser_factory('current_period_end')
put_current_period_end = nullable_date_time_optional_putter_factory('current_period_end')
validate_current_period_end = nullable_date_time_validator_factory('current_period_end')


# current_period_start

parse_current_period_start = nullable_date_time_parser_factory('current_period_start')
put_current_period_start = nullable_date_time_optional_putter_factory('current_period_start')
validate_current_period_start = nullable_date_time_validator_factory('current_period_start')


# entitlement_ids

parse_entitlement_ids = entity_id_array_parser_factory('entitlement_ids')
put_entitlement_ids = optional_entity_id_array_optional_putter_factory('entitlement_ids')
validate_entitlement_ids = entity_id_array_validator_factory('entitlement_ids', NotImplemented, include = 'Entitlement')


# id

parse_id = entity_id_parser_factory('id')
put_id = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('subscription_id')


# renewal_sku_ids

parse_renewal_sku_ids = entity_id_array_parser_factory('renewal_sku_ids')
put_renewal_sku_ids = optional_entity_id_array_optional_putter_factory('renewal_sku_ids')
validate_renewal_sku_ids = entity_id_array_validator_factory('renewal_sku_ids', SKU)


# sku_idpa

validate_sku_id = entity_id_validator_factory('sku_id', SKU)


# sku_ids

parse_sku_ids = entity_id_array_parser_factory('sku_ids')
put_sku_ids = optional_entity_id_array_optional_putter_factory('sku_ids')
validate_sku_ids = entity_id_array_validator_factory('sku_ids', SKU)


# status

parse_status = preinstanced_parser_factory('status', SubscriptionStatus, SubscriptionStatus.active)
put_status = preinstanced_putter_factory('status')
validate_status = preinstanced_validator_factory('status', SubscriptionStatus)


# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id = entity_id_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
