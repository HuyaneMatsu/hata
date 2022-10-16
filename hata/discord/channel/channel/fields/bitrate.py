__all__ = ()

from ....field_parsers import int_parser_factory
from ....field_putters import int_putter_factory
from ....field_validators import int_conditional_validator_factory

from ..constants import BITRATE_DEFAULT, BITRATE_MAX, BITRATE_MIN


parse_bitrate = int_parser_factory('bitrate', BITRATE_DEFAULT)
put_bitrate_into = int_putter_factory('bitrate')
validate_bitrate = int_conditional_validator_factory(
    'bitrate',
    (lambda bitrate: bitrate >= BITRATE_MIN and bitrate <= BITRATE_MAX),
    f'>= {BITRATE_MIN} and <= {BITRATE_MAX},'
)
