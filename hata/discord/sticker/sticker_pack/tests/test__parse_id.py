import vampytest

from ..fields import parse_id


def test__parse_id():
    """
    Tests whether ``parse_id`` works as intended.
    """
    sticker_pack_id = 202301050000
    
    for input_data, expected_output in (
        ({}, 0),
        ({'id': None}, 0),
        ({'id': str(sticker_pack_id)}, sticker_pack_id),
    ):
        output = parse_id(input_data)
        vampytest.assert_eq(output, expected_output)
