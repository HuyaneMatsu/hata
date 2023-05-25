__all__ = ()

from ...channel import Channel
from ...emoji import Emoji, create_partial_emoji_from_inline_data, put_partial_emoji_inline_data_into
from ...field_parsers import entity_id_parser_factory, nullable_string_parser_factory
from ...field_putters import (
    entity_id_putter_factory, nullable_functional_optional_putter_factory, nullable_string_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, nullable_entity_validator_factory, nullable_string_validator_factory
)

from .constants import DESCRIPTION_LENGTH_MAX

# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', Channel)

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)

# emoji

parse_emoji = create_partial_emoji_from_inline_data


def put_emoji_into(emoji, data, defaults):
    """
    Puts the emoji into the given `data` json serializable object.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        The emoji.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or (emoji is not None):
        put_partial_emoji_inline_data_into(emoji, data)
    
    return data


validate_emoji = nullable_entity_validator_factory('emoji', Emoji)
