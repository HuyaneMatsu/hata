__all__ = ()

from ...field_parsers import entity_id_parser_factory, nullable_unix_time_parser_factory
from ...field_putters import entity_id_optional_putter_factory, nullable_unix_time_optional_putter_factory
from ...field_validators import entity_id_validator_factory, nullable_date_time_validator_factory

# sku_id

parse_sku_id = entity_id_parser_factory('sku_id')
put_sku_id = entity_id_optional_putter_factory('sku_id')
validate_sku_id = entity_id_validator_factory('sku_id', NotImplemented, include = 'SKU')


# expires_at

parse_expires_at = nullable_unix_time_parser_factory('expires_at')
put_expires_at = nullable_unix_time_optional_putter_factory('expires_at')
validate_expires_at = nullable_date_time_validator_factory('expires_at')
