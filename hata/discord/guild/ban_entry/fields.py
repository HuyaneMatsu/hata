__all__ = ()

from ...field_parsers import default_entity_parser_factory, nullable_string_parser_factory
from ...field_putters import default_entity_putter_factory, nullable_string_optional_putter_factory
from ...field_validators import default_entity_validator_factory, nullable_string_validator_factory
from ...user import ClientUserBase, User, ZEROUSER

from .constants import REASON_LENGTH_MAX, REASON_LENGTH_MIN

# user

parse_user = default_entity_parser_factory('user', User, default = ZEROUSER)
put_user = default_entity_putter_factory('user', ClientUserBase, ZEROUSER, force_include_internals = True)
validate_user = default_entity_validator_factory('user', ClientUserBase, default = ZEROUSER)

# reason

parse_reason = nullable_string_parser_factory('reason')
put_reason = nullable_string_optional_putter_factory('reason')
validate_reason = nullable_string_validator_factory('reason', REASON_LENGTH_MIN, REASON_LENGTH_MAX)
