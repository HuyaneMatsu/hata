__all__ = ()

from ....field_validators import nullable_entity_validator
from ....emoji import Emoji, create_emoji_from_exclusive_data, put_exclusive_emoji_data_into


def parse_default_thread_reaction(data):
    """
    Parses out the `default_thread_reaction` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    default_thread_reaction : `None`, ``Emoji``
    """
    default_thread_reaction_data = data.get('default_reaction_emoji', None)
    if (default_thread_reaction_data is None):
        default_thread_reaction = None
    else:
        default_thread_reaction = create_emoji_from_exclusive_data(default_thread_reaction_data)
    
    return default_thread_reaction


def put_default_thread_reaction_into(default_thread_reaction, data, defaults):
    """
    Puts the `default_thread_reaction`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    default_thread_reaction : `None`, ``Emoji``
        The emoji to show in the add reaction button on a thread of the forum channel.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (default_thread_reaction is not None):
        if default_thread_reaction is None:
            emoji_data = None
        else:
            emoji_data = put_exclusive_emoji_data_into(default_thread_reaction, {})
        
        data['default_reaction_emoji'] = emoji_data
    
    return data


validate_default_thread_reaction = nullable_entity_validator('default_thread_reaction', Emoji)
