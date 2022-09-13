__all__ = ()

from ...emoji import Emoji, create_emoji_from_exclusive_data


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
    

def validate_default_thread_reaction(default_thread_reaction):
    """
    Validates the given `default_thread_reaction` field.
    
    Parameters
    ----------
    default_thread_reaction : `None`, ``Emoji``
        The emoji to validate.
    
    Returns
    -------
    default_thread_reaction : `None`, ``Emoji``
    
    Raises
    ------
    TypeError
        - If `default_thread_reaction` is not `None`, ``Emoji``
    """
    if (default_thread_reaction is not None) and (not isinstance(default_thread_reaction, Emoji)):
        raise TypeError(
            f'`default_thread_reaction` can be `None`, `{Emoji.__name__}`, '
            f'got {default_thread_reaction.__class__.__name__}; {default_thread_reaction!r}.'
        )
    
    return default_thread_reaction
