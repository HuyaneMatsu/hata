__all__ = ()

from ....field_parsers import bool_parser_factory
from ....field_putters import bool_optional_putter_factory
from ....field_validators import bool_validator_factory


parse_nsfw = bool_parser_factory('nsfw', False)
put_nsfw_into = bool_optional_putter_factory('nsfw', False)
validate_nsfw = bool_validator_factory('nsfw')
