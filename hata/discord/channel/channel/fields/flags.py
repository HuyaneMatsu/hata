__all__ = ()

from ....field_parsers import flag_parser_factory
from ....field_putters import flag_optional_putter_factory
from ....field_validators import flag_validator_factory

from ..flags import ChannelFlag

parse_flags = flag_parser_factory('flags', ChannelFlag)
put_flags_into = flag_optional_putter_factory('flags', ChannelFlag())
validate_flags = flag_validator_factory('flags', ChannelFlag)
