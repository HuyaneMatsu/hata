__all__ = ()

from ..flags import ChannelFlag


def parse_flags(data):
    """
    Parses out the `flags` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    flags : ``ChannelFlag``
    """
    return ChannelFlag(data.get('flags', 0))
