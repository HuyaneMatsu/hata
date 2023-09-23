__all__ = ()

from ...field_parsers import bool_parser_factory
from ...field_putters import bool_optional_putter_factory
from ...field_validators import bool_validator_factory

# emoji_pack_collectible

parse_emoji_pack_collectible = bool_parser_factory('is_emoji_pack_collectible', False)
put_emoji_pack_collectible_into = bool_optional_putter_factory('is_emoji_pack_collectible', False)
validate_emoji_pack_collectible = bool_validator_factory('emoji_pack_collectible', False)
