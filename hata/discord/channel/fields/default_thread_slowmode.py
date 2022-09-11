__all__ = ()


def parse_default_thread_slowmode(data):
    """
    Parses out the `default_thread_slowmode` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    default_thread_slowmode : `int`
    """
    default_thread_slowmode = data.get('default_thread_rate_limit_per_user', None)
    if default_thread_slowmode is None:
        default_thread_slowmode = 0
    
    return default_thread_slowmode
