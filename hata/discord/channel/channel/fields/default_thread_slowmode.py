__all__ = ()

from ....field_parsers import int_parser_factory
from ....field_putters import nullable_int_optional_putter_factory
from ....field_validators import int_conditional_validator_factory

from ..constants import SLOWMODE_DEFAULT, SLOWMODE_MAX, SLOWMODE_MIN


parse_default_thread_slowmode = int_parser_factory('default_thread_rate_limit_per_user', SLOWMODE_DEFAULT)
put_default_thread_slowmode_into = nullable_int_optional_putter_factory(
    'default_thread_rate_limit_per_user',
    SLOWMODE_DEFAULT,
)
validate_default_thread_slowmode = int_conditional_validator_factory(
    'default_thread_slowmode',
    (
        lambda default_thread_slowmode:
        default_thread_slowmode >= SLOWMODE_MIN and default_thread_slowmode <= SLOWMODE_MAX
    ),
    f'>= {SLOWMODE_MIN} and <= {SLOWMODE_MAX},'
)
