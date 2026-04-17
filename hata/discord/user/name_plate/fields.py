__all__ = ()

from ...field_parsers import (
    entity_id_parser_factory, force_string_parser_factory, nullable_unix_time_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_optional_putter_factory, force_string_putter_factory, nullable_unix_time_optional_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, force_string_validator_factory, nullable_date_time_validator_factory,
    preinstanced_validator_factory
)

from .preinstanced import Palette

# asset_path

parse_asset_path = force_string_parser_factory('asset')
put_asset_path = force_string_putter_factory('asset')
validate_asset_path = force_string_validator_factory('asset_path', 0, 1024)


# expires_at

parse_expires_at = nullable_unix_time_parser_factory('expires_at')
put_expires_at = nullable_unix_time_optional_putter_factory('expires_at')
validate_expires_at = nullable_date_time_validator_factory('expires_at')


# name

parse_name = force_string_parser_factory('label')
put_name = force_string_putter_factory('label')
validate_name = force_string_validator_factory('name', 0, 1024)


# palette

parse_palette = preinstanced_parser_factory('palette', Palette, Palette.black)
put_palette = preinstanced_putter_factory('palette')
validate_palette = preinstanced_validator_factory('palette', Palette)


# sku_id

parse_sku_id = entity_id_parser_factory('sku_id')
put_sku_id = entity_id_optional_putter_factory('sku_id')
validate_sku_id = entity_id_validator_factory('sku_id', NotImplemented, include = 'SKU')
