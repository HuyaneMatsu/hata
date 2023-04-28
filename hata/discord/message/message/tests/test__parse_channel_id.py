import vampytest

from ..fields import parse_channel_id


def test__parse_channel_id():
    """
    Tests whether ``parse_channel_id`` works as intended.
    """
    channel_id = 202304260003
    
    for input_data, expected_output in (
        ({}, 0),
        ({'channel_id': None}, 0),
        ({'channel_id': str(channel_id)}, channel_id),
    ):
        output = parse_channel_id(input_data)
        vampytest.assert_eq(output, expected_output)
