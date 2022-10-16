__all__ = ()

from ....field_parsers import int_parser_factory
from ....field_putters import int_putter_factory
from ....field_validators import int_conditional_validator_factory

from ..constants import USER_LIMIT_DEFAULT, USER_LIMIT_MAX, USER_LIMIT_MIN


parse_user_limit = int_parser_factory('user_limit', USER_LIMIT_DEFAULT)
put_user_limit_into = int_putter_factory('user_limit')
validate_user_limit = int_conditional_validator_factory(
    'user_limit',
    (lambda user_limit: user_limit >= USER_LIMIT_MIN and user_limit <= USER_LIMIT_MAX),
    f'>= {USER_LIMIT_MIN} and <= {USER_LIMIT_MAX},'
)
