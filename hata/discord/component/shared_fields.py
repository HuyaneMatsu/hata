__all__ = ()


from ..emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data
from ..field_parsers import (
    nullable_functional_parser_factory, nullable_object_array_parser_factory, nullable_string_parser_factory
)
from ..field_putters import (
    nullable_entity_array_putter_factory, nullable_functional_optional_putter_factory, url_optional_putter_factory
)
from ..field_validators import (
    nullable_entity_validator_factory, nullable_object_array_validator_factory, nullable_string_validator_factory
)

from .shared_constants import CUSTOM_ID_LENGTH_MAX

# components

parse_components = nullable_object_array_parser_factory('components', NotImplemented, include = 'Component')
put_components_into = nullable_entity_array_putter_factory('components', NotImplemented, include = 'Component')
validate_components = nullable_object_array_validator_factory('components', NotImplemented, include = 'Component')

# custom_id

parse_custom_id = nullable_string_parser_factory('custom_id')
put_custom_id_into = url_optional_putter_factory('custom_id')
validate_custom_id = nullable_string_validator_factory('custom_id', 0, CUSTOM_ID_LENGTH_MAX)

# emoji

parse_emoji = nullable_functional_parser_factory('emoji', create_partial_emoji_from_data)
put_emoji_into = nullable_functional_optional_putter_factory('emoji', create_partial_emoji_data)
validate_emoji = nullable_entity_validator_factory('emoji', Emoji)
