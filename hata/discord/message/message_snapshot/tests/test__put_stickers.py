import vampytest

from ....sticker import Sticker, StickerFormat, create_partial_sticker_data

from ..fields import put_stickers


def _iter_options():
    sticker_id_0 = 202409200042
    sticker_name_0 = 'Orin'
    sticker_format_0 = StickerFormat.png
    
    sticker_id_1 = 202409200043
    sticker_name_1 = 'Okuu'
    sticker_format_1 = StickerFormat.apng
    
    sticker_0 = Sticker.precreate(sticker_id_0, name = sticker_name_0, sticker_format = sticker_format_0)
    sticker_1 = Sticker.precreate(sticker_id_1, name = sticker_name_1, sticker_format = sticker_format_1)
    
    yield None, False, {}
    yield None, True, {'message': {'sticker_items': []}}
    
    yield (sticker_0,), False, {'message': {'sticker_items': [create_partial_sticker_data(sticker_0)]}}
    yield (sticker_0,), True, {'message': {'sticker_items': [create_partial_sticker_data(sticker_0)]}}
    
    yield (
        (sticker_0, sticker_1),
        False,
        {'message': {'sticker_items': [create_partial_sticker_data(sticker_0), create_partial_sticker_data(sticker_1)]}},
    )
    yield (
        (sticker_0, sticker_1),
        True,
        {'message': {'sticker_items': [create_partial_sticker_data(sticker_0), create_partial_sticker_data(sticker_1)]}},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_stickers(input_value, defaults):
    """
    Tests whether ``put_stickers`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<Sticker>`
        Input value to serialise.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_stickers(input_value, {}, defaults)
