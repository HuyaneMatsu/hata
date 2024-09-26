import vampytest

from ....sticker import Sticker, StickerFormat

from ..fields import parse_stickers


def _iter_options():
    yield {}
    yield {'message': None}
    yield {'message': {}}
    yield {'message': {'sticker_items': None}}
    yield {'message': {'sticker_items': {}}}


@vampytest.call_from(_iter_options())
def test__parse_stickers__no_data(input_data):
    """
    Tests whether ``parse_stickers`` works as intended.
    
    Case: No data.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    """
    output = parse_stickers(input_data)
    vampytest.assert_is(output, None)


def test__parse_stickers__with_data():
    """
    Tests whether ``parse_stickers`` works as intended.
    
    Case: With data.
    """
    sticker_id_0 = 202409200040
    sticker_name_0 = 'Orin'
    sticker_format_0 = StickerFormat.png
    
    sticker_id_1 = 202409200041
    sticker_name_1 = 'Okuu'
    sticker_format_1 = StickerFormat.apng
    
    input_data = {
        'message': {
            'sticker_items': [
                {
                    'id': str(sticker_id_0),
                    'name': sticker_name_0,
                    'format_type': sticker_format_0.value,
                }, {
                    'id': str(sticker_id_1),
                    'name': sticker_name_1,
                    'format_type': sticker_format_1.value,
                },
            ],
        },
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
