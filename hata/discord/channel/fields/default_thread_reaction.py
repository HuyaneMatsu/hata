__all__ = ()

from ...emoji import create_emoji_from_exclusive_data


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
    
