import vampytest

from ..fields import put_cover_sticker_id


def test__put_cover_sticker_id():
    """
    Tests whether ``put_cover_sticker_id`` works as intended.
    """
    cover_sticker_id = 202301040009
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'cover_sticker_id': None}),
        (cover_sticker_id, False, {'cover_sticker_id': str(cover_sticker_id)}),
    ):
        output = put_cover_sticker_id(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
