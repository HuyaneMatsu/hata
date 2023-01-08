__all__ = ()

from ...field_parsers import entity_id_parser_factory, force_string_parser_factory, nullable_string_parser_factory
from ...field_putters import (
    entity_id_optional_putter_factory, entity_id_putter_factory, force_string_putter_factory,
    nullable_string_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, force_string_validator_factory, nullable_string_validator_factory
)

from ..sticker import Sticker

# banner_id

parse_banner_id = entity_id_parser_factory('banner_asset_id')
put_banner_id_into = entity_id_optional_putter_factory('banner_asset_id')
validate_banner_id = entity_id_validator_factory('banner_id')

# cover_sticker_id

parse_cover_sticker_id = entity_id_parser_factory('cover_sticker_id')
put_cover_sticker_id_into = entity_id_optional_putter_factory('cover_sticker_id')
validate_cover_sticker_id = entity_id_validator_factory('cover_sticker_id', Sticker)

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, 1024)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('id')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', 0, 1024)

# sku_id

parse_sku_id = entity_id_parser_factory('sku_id')
put_sku_id_into = entity_id_optional_putter_factory('sku_id')
validate_sku_id = entity_id_validator_factory('sku_id')

# stickers

def parse_stickers(data):
    """
    Parses the stickers out from the given sticker-pack data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Sticker-pack data.
    
    Returns
    -------
    stickers : `None``, `frozenset` of ``Sticker``
    """
    sticker_datas = data.get('stickers', None)
    if (sticker_datas is not None) and sticker_datas:
        return frozenset(Sticker.from_data(sticker_data) for sticker_data in sticker_datas)


def put_stickers_into(stickers, data, defaults):
    """
    Puts the stickers into the given json serializable dictionary.
    
    Parameters
    ----------
    stickers : `None`, `frozenset` of `Sticker`
        Stickers.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if stickers is None:
        sticker_datas = []
    else:
        sticker_datas = [sticker.to_data(defaults = defaults, include_internals = True) for sticker in stickers]
    data['stickers'] = sticker_datas
    return data


def validate_stickers(stickers):
    """
    Validates the given stickers.
    
    Parameters
    ----------
    stickers : `None`, `iterable` of ``Sticker``
        The stickers to validate.
    
    Returns
    -------
    stickers : `None`, `frozenset` of ``Sticker``
        The validated stickers.
    
    Raises
    ------
    TypeError
        - If `sticker` is not `None`, `iterable` of ``Sticker``.
        - If `sticker` contains a non-``Sticker`` element. 
    """
    if stickers is None:
        return None
    
    if getattr(type(stickers), '__iter__', None) is None:
        raise TypeError(
            f'`stickers` can be `None` ot `iterable` of `{Sticker.__name__}`, '
            f'got {stickers.__class__.__name__}; {stickers!r}.'
        )
    
    validated_stickers = None
    
    for sticker in stickers:
        if not isinstance(sticker, Sticker):
            raise TypeError(
                f'`sticker` can contain `{Sticker.__name__}` elements, got {sticker.__class__.__name__}; {sticker!r}; '
                f'stickers = {stickers!r}.'
            )
        
        if (validated_stickers is None):
            validated_stickers = set()
        
        validated_stickers.add(sticker)
    
    if (validated_stickers is not None):
        return frozenset(validated_stickers)
