__all__ = ()

from ...emoji import Emoji, create_partial_emoji_from_inline_data, put_partial_emoji_inline_data_into
from ...field_parsers import force_string_parser_factory
from ...field_putters import force_string_putter_factory
from ...field_validators import force_string_validator_factory, nullable_entity_validator_factory

from .constants import TITLE_LENGTH_MAX, TITLE_LENGTH_MIN

# emoji

parse_emoji = create_partial_emoji_from_inline_data


def put_emoji(emoji, data, defaults):
    """
    Puts the emoji into the given `data` json serializable object.
    
    Parameters
    ----------
    emoji : ``None | Emoji``
        The emoji.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (emoji is not None):
        put_partial_emoji_inline_data_into(emoji, data)
    
    return data


validate_emoji = nullable_entity_validator_factory('emoji', Emoji)


# title

parse_title = force_string_parser_factory('label')
put_title = force_string_putter_factory('label')
validate_title = force_string_validator_factory('title', TITLE_LENGTH_MIN, TITLE_LENGTH_MAX)
