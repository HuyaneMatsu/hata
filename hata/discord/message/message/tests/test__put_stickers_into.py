import vampytest

from ....sticker import Sticker, StickerFormat, create_partial_sticker_data

from ..fields import put_stickers_into


def test__put_stickers_into__1():
    """
    Tests whether ``put_stickers_into`` works as intended.
    
    Case: Nothing.
    """
    sticker_id_0 = 202305010010
    sticker_id_1 = 202305010011
    sticker_name_0 = 'Orin'
    sticker_name_1 = 'Okuu'
    sticker_format_0 = StickerFormat.png
    sticker_format_1 = StickerFormat.apng
    
    sticker_0 = Sticker.precreate(sticker_id_0, name = sticker_name_0, sticker_format = sticker_format_0)
    sticker_1 = Sticker.precreate(sticker_id_1, name = sticker_name_1, sticker_format = sticker_format_1)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'sticker_items': []}),
        ((sticker_0,), False, {'sticker_items': [create_partial_sticker_data(sticker_0)]}),
        (
            (sticker_0, sticker_1),
            False,
            {'sticker_items': [create_partial_sticker_data(sticker_0), create_partial_sticker_data(sticker_1)]},
        ),
    ):
        output = put_stickers_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
