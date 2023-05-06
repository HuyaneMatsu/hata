import vampytest

from ....sticker import Sticker, StickerFormat

from ..fields import parse_stickers


def test__parse_stickers__0():
    """
    Tests whether ``parse_stickers`` works as intended.
    
    Case: Nothing.
    """
    for input_data in (
        {},
        {'sticker_items': None},
        {'sticker_items': []},
    ):
        output = parse_stickers(input_data)
        vampytest.assert_is(output, None)


def test__parse_stickers__1():
    """
    Tests whether ``parse_stickers`` works as intended.
    
    Case: Nothing.
    """
    sticker_id_0 = 202305010009
    sticker_id_1 = 202305010008
    sticker_name_0 = 'Orin'
    sticker_name_1 = 'Okuu'
    sticker_format_0 = StickerFormat.png
    sticker_format_1 = StickerFormat.apng
    
    input_data = {
        'sticker_items': [
            {
                'id': str(sticker_id_0),
                'name': sticker_name_0,
                'format_type': sticker_format_0.value,
            }, {
                'id': str(sticker_id_1),
                'name': sticker_name_1,
                'format_type': sticker_format_1.value,
            }
        ]
    }
    
    output = parse_stickers(input_data)
    vampytest.assert_is_not(output, None)
    vampytest.assert_instance(output, tuple)
    
    vampytest.assert_instance(output[0], Sticker)
    vampytest.assert_eq(output[0].id, sticker_id_0)
    vampytest.assert_eq(output[0].name, sticker_name_0)
    vampytest.assert_is(output[0].format, sticker_format_0)
    
    vampytest.assert_instance(output[1], Sticker)
    vampytest.assert_eq(output[1].id, sticker_id_1)
    vampytest.assert_eq(output[1].name, sticker_name_1)
    vampytest.assert_is(output[1].format, sticker_format_1)
