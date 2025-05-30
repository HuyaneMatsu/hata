__all__ = ('create_partial_sticker_data', 'create_partial_sticker_from_id', 'create_partial_sticker_from_partial_data')


from .fields import put_format, put_id, put_name, parse_id, parse_format, parse_name
from .sticker import Sticker
from ...core import STICKERS


def create_partial_sticker_data(sticker):
    """
    Creates partial sticker data for the given sticker.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The sticker to create the partial data from.
    
    Returns
    ------
    data : `dict<str, object>`
    """
    data = {}
    put_format(sticker.format, data, True)
    put_id(sticker.id, data, True)
    put_name(sticker.name, data, True)
    return data


def create_partial_sticker_from_partial_data(data):
    """
    Creates a sticker from the given partial sticker data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Sticker data.
    
    Returns
    -------
    sticker : ``Sticker``
    """
    sticker_id = parse_id(data)
    
    try:
        sticker = STICKERS[sticker_id]
    except KeyError:
        sticker = Sticker._create_empty(sticker_id)
        STICKERS[sticker_id] = sticker
    else:
        if not sticker.partial:
            return sticker
    
    sticker.format = parse_format(data)
    sticker.name = parse_name(data)
    
    return sticker


def create_partial_sticker_from_id(sticker_id):
    """
    Creates a sticker from the given identifier.
    
    Parameters
    ----------
    sticker_id : `int`
        The identifier to create the sticker for.
    
    Returns
    -------
    sticker : ``Sticker``
    """
    try:
        sticker = STICKERS[sticker_id]
    except KeyError:
        sticker = Sticker._create_empty(sticker_id)
        STICKERS[sticker_id] = sticker
    
    return sticker
