import vampytest

from ..fields import parse_channel_id


def test__parse_channel_id():
    """
    Tests whether ``parse_channel_id`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'channel_id': None}, 0),
        ({'channel_id': '1'}, 1),
    ):
        output = parse_channel_id(input_data)
        vampytest.assert_eq(output, expected_output)
