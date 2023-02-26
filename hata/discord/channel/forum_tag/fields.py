__all__ = ()

from ...emoji import Emoji, create_emoji_from_exclusive_data, put_exclusive_emoji_data_into
from ...field_parsers import entity_id_parser_factory, force_string_parser_factory, bool_parser_factory
from ...field_putters import entity_id_putter_factory, force_string_putter_factory, bool_optional_putter_factory
from ...field_validators import entity_id_validator_factory, force_string_validator_factory, bool_validator_factory

from .constants import NAME_LENGTH_MIN, NAME_LENGTH_MAX

# emoji

def put_emoji_into(emoji, data, defaults):
    """
    Puts the `emoji`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        The forum tag's emoji.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (emoji is not None):
        put_exclusive_emoji_data_into(emoji, data)
    
    return data


def parse_emoji(data):
    """
    Parses out the `emoji` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    return create_emoji_from_exclusive_data(data)


def validate_emoji(emoji):
    """
    Validates the given `emoji` field.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        The emoji of the forum tag.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    
    Raises
    ------
    TypeError
        - If `emoji` is not `None`, ``Emoji``
    """
    if (emoji is not None) and (not isinstance(emoji, Emoji)):
        raise TypeError(
            f'`emoji` can be `None`, `{Emoji.__name__}`, got {emoji.__class__.__name__}; {emoji!r}.'
        )
    
    return emoji

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
