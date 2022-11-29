__all__ = ()

from ...field_parsers import force_string_parser_factory
from ...field_putters import force_string_putter_factory
from ...field_validators import force_string_validator_factory

# distributor

parse_distributor = force_string_parser_factory('distributor')
put_distributor_into = force_string_putter_factory('distributor')
validate_distributor = force_string_validator_factory('distributor', 0, 1024)

# id

parse_id = force_string_parser_factory('id')
put_id_into = force_string_putter_factory('id')
validate_id = force_string_validator_factory('sku_id', 0, 1024)

# sku

parse_sku = force_string_parser_factory('sku')
put_sku_into = force_string_putter_factory('sku')
validate_sku = force_string_validator_factory('sku', 0, 1024)
