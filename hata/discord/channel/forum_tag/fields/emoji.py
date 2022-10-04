__all__ = ()

from ....emoji import Emoji, create_emoji_from_exclusive_data, put_exclusive_emoji_data_into


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
