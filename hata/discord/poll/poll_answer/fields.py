__all__ = ()

from ...emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data
from ...field_parsers import entity_id_parser_factory
from ...field_putters import entity_id_putter_factory
from ...field_validators import (
    entity_id_validator_factory, nullable_entity_validator_factory, nullable_string_validator_factory
)

from .constants import TEXT_LENGTH_MAX


# emoji

def parse_emoji(data):
    """
    Parses out the `emoji` field from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Channel data.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    nested_data = data.get('poll_media', None)
    if nested_data is None:
        return None
    
    emoji_data = nested_data.get('emoji', None)
    if emoji_data is None:
        return None
    
    return create_partial_emoji_from_data(emoji_data)


def put_emoji_into(emoji, data, defaults):
    """
    Puts the `emoji`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        The emoji to serialize.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (emoji is not None):
        nested_data = data.get('poll_media', None)
        if nested_data is None:
            nested_data = {}
            data['poll_media'] = nested_data
        
        if emoji is None:
            emoji_data = None
        else:
            emoji_data = create_partial_emoji_data(emoji)
        
        nested_data['emoji'] = emoji_data
    
    return data


validate_emoji = nullable_entity_validator_factory('emoji', Emoji)

# id

parse_id = entity_id_parser_factory('answer_id')
put_id_into = entity_id_putter_factory('answer_id')
validate_id = entity_id_validator_factory('answer_id')

# text

def parse_text(data):
    """
    Parses out a poll answer's text from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Poll answer data.
    
    Returns
    -------
    text : `None | str`
    """
    nested_data = data.get('poll_media', None)
    if nested_data is None:
        return None
    
    text = nested_data.get('text', None)
    if (text is None) or (not text):
        return None
    
    return text


def put_text_into(text, data, defaults):
    """
    Serializes the given text into the given data.
    
    Parameters
    ----------
    text : `None | str`
        Poll answer text.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    nested_data = data.get('poll_media', None)
    if nested_data is None:
        nested_data = {}
        data['poll_media'] = nested_data
    
    if text is None:
        text = ''
    
    nested_data['text'] = text
    return data


validate_text = nullable_string_validator_factory('text', 0, TEXT_LENGTH_MAX)
