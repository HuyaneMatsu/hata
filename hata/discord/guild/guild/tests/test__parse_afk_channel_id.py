import vampytest

from ..fields import parse_afk_channel_id


def test__parse_afk_channel_id():
    """
    Tests whether ``parse_afk_channel_id`` works as intended.
    """
    afk_channel_id = 202306080000
    
    for input_data, expected_output in (
        ({}, 0),
        ({'afk_channel_id': None}, 0),
        ({'afk_channel_id': str(afk_channel_id)}, afk_channel_id),
    ):
        output = parse_afk_channel_id(input_data)
        vampytest.assert_eq(output, expected_output)
