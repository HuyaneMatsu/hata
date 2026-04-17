import vampytest

from ..fields import parse_cover_sticker_id


def test__parse_cover_sticker_id():
    """
    Tests whether ``parse_cover_sticker_id`` works as intended.
    """
    cover_sticker_id = 202301050008
    
    for input_data, expected_output in (
        ({}, 0),
        ({'cover_sticker_id': None}, 0),
        ({'cover_sticker_id': str(cover_sticker_id)}, cover_sticker_id),
    ):
        output = parse_cover_sticker_id(input_data)
        vampytest.assert_eq(output, expected_output)
