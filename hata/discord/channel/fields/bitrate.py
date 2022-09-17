__all__ = ()

from ...preconverters import preconvert_int

from ..constants import BITRATE_DEFAULT, BITRATE_MAX, BITRATE_MIN


def parse_bitrate(data):
    """
    Parses out the `bitrate` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    bitrate : `int`
    """
    return data.get('bitrate', BITRATE_DEFAULT)


def validate_bitrate(bitrate):
    """
    Validates the given `bitrate` field.
    
    Parameters
    ----------
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    
    Returns
    -------
    bitrate : `int`
    
    Raises
    ------
    TypeError
        - If `bitrate` is not `int`.
    ValueError
        - If `bitrate` is out of the expected range.
    """
    return preconvert_int(bitrate, 'bitrate', BITRATE_MIN, BITRATE_MAX)


def put_bitrate_into(bitrate, data, defaults):
    """
    Puts the `bitrate`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['bitrate'] = bitrate
    
    return data
