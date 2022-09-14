__all__ = ()

from ...preconverters import preconvert_flag

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


def validate_flags(flags):
    """
    Validates the given `flags` field.
    
    Parameters
    ----------
    flags : `int`, ``ChannelFlag``
        Channel flags.
    
    Returns
    -------
    flags : ``ChannelFlag``
    
    Raises
    ------
    TypeError
        - If `flags` is not `int`.
    """
    return preconvert_flag(flags, 'flags', ChannelFlag)


def put_flags_into(flags, data, defaults):
    """
    Puts the `flags`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    flags : ``ChannelFlag``
        The channel's flags.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if flags:
        data['flags'] = int(flags)
    
    else:
        if defaults:
            data['flags'] = 0
    
    return data
