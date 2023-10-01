__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, flag_parser_factory, force_string_parser_factory,
    nullable_date_time_parser_factory, nullable_string_parser_factory, preinstanced_array_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_putter_factory, flag_optional_putter_factory, force_string_putter_factory,
    nullable_date_time_optional_putter_factory, preinstanced_array_putter_factory, preinstanced_putter_factory,
    url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, flag_validator_factory, force_string_validator_factory,
    nullable_date_time_validator_factory, preinstanced_array_validator_factory, preinstanced_validator_factory,
    url_optional_validator_factory
)

from ..application import Application

from .constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN
from .flags import SKUFlag
from .preinstanced import SKUAccessType, SKUFeature, SKUType

# access_type

parse_access_type = preinstanced_parser_factory('access_type', SKUAccessType, SKUAccessType.none)
put_access_type_into = preinstanced_putter_factory('access_type')
validate_access_type = preinstanced_validator_factory('access_type', SKUAccessType)

# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id_into = entity_id_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', Application)

# features

parse_features = preinstanced_array_parser_factory('features', SKUFeature)
put_features_into = preinstanced_array_putter_factory('features')
validate_features = preinstanced_array_validator_factory('features', SKUFeature)

# flags

parse_flags = flag_parser_factory('flags', SKUFlag)
put_flags_into = flag_optional_putter_factory('flags', SKUFlag())
validate_flags = flag_validator_factory('flags', SKUFlag)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('sku_id')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# premium

parse_premium = bool_parser_factory('premium', False)
put_premium_into = bool_optional_putter_factory('premium', False)
validate_premium = bool_validator_factory('premium', False)

# release_at

parse_release_at = nullable_date_time_parser_factory('release_date')
put_release_at_into = nullable_date_time_optional_putter_factory('release_date')
validate_release_at = nullable_date_time_validator_factory('release_at')

# slug

parse_slug = nullable_string_parser_factory('slug')
put_slug_into = url_optional_putter_factory('slug')
validate_slug = url_optional_validator_factory('slug')

# type

parse_type = preinstanced_parser_factory('type', SKUType, SKUType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('sku_type', SKUType)
