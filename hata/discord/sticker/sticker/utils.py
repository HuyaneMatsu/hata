__all__ = ('create_partial_sticker_data', 'create_partial_sticker_from_partial_data')


from .fields import put_format_into, put_id_into, put_name_into, parse_id, parse_format, parse_name
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
    -------
    data : `dict` of (`str`, `object`) items
    """
    data = {}
    put_format_into(sticker.format, data, True)
    put_id_into(sticker.id, data, True)
    put_name_into(sticker.name, data, True)
    return data


def create_partial_sticker_from_partial_data(data):
    """
    Creates a sticker from the given partial sticker data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Sticker data.
    
    Returns
    -------
    sticker : `instance<cls>`
    """
    sticker_id = parse_id(data)
    
    try:
        self = STICKERS[sticker_id]
    except KeyError:
        self = Sticker._create_empty(sticker_id)
        STICKERS[sticker_id] = self
    else:
        if not self.partial:
            return self
    
    self.format = parse_format(data)
    self.name = parse_name(data)
    
    return self
