__all__ = ()

from ....field_parsers import int_parser_factory
from ....field_putters import int_putter_factory
from ....field_validators import int_conditional_validator_factory


parse_position = int_parser_factory('position', 0)
put_position_into = int_putter_factory('position')
validate_position = int_conditional_validator_factory(
    'position',
    lambda position : position >= 0,
    '>= 0',
)
