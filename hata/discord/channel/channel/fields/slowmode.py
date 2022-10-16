__all__ = ()

from ....field_parsers import int_parser_factory
from ....field_putters import nullable_int_optional_putter_factory
from ....field_validators import int_conditional_validator_factory

from ..constants import SLOWMODE_DEFAULT, SLOWMODE_MAX, SLOWMODE_MIN


parse_slowmode = int_parser_factory('rate_limit_per_user', SLOWMODE_DEFAULT)
put_slowmode_into = nullable_int_optional_putter_factory(
    'rate_limit_per_user',
    SLOWMODE_DEFAULT,
)
validate_slowmode = int_conditional_validator_factory(
    'slowmode',
    (
        lambda slowmode:
        slowmode >= SLOWMODE_MIN and slowmode <= SLOWMODE_MAX
    ),
    f'>= {SLOWMODE_MIN} and <= {SLOWMODE_MAX},'
)
