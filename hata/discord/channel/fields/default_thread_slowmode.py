__all__ = ()

from ...preconverters import preconvert_int

from ..constants import SLOWMODE_MAX, SLOWMODE_MIN


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


def validate_default_thread_slowmode(default_thread_slowmode):
    """
    Validates the given `default_thread_slowmode` field.
    
    Parameters
    ----------
    default_thread_slowmode : `int`
        Slowmode applied for created threads in the channel.
    
    Returns
    -------
    default_thread_slowmode : `int`
    
    Raises
    ------
    TypeError
        - If `default_thread_slowmode` is not `int`.
    ValueError
        - If `default_thread_slowmode` is out of the expected range.
    """
    return preconvert_int(default_thread_slowmode, 'default_thread_slowmode', SLOWMODE_MIN, SLOWMODE_MAX)
