__all__ = ()

from ...emoji import Emoji, create_emoji_from_exclusive_data, put_exclusive_emoji_data_into
from ...field_parsers import bool_parser_factory, entity_id_parser_factory, force_string_parser_factory
from ...field_putters import bool_optional_putter_factory, entity_id_putter_factory, force_string_putter_factory
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, force_string_validator_factory,
    nullable_entity_validator_factory
)

from .constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN

# emoji

def parse_emoji(data):
    """
    Parses out the `emoji` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Channel data.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    return create_emoji_from_exclusive_data(data)


def put_emoji_into(emoji, data, defaults):
    """
    Puts the `emoji`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        The forum tag's emoji.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or (emoji is not None):
        put_exclusive_emoji_data_into(emoji, data)
    
    return data


validate_emoji = nullable_entity_validator_factory('emoji', Emoji)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('forum_tag_id')

# moderated

parse_moderated = bool_parser_factory('moderated', False)
put_moderated_into = bool_optional_putter_factory('moderated', False)
validate_moderated = bool_validator_factory('moderated', False)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)
