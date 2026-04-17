import vampytest

from ..fields import parse_system_channel_id


def test__parse_system_channel_id():
    """
    Tests whether ``parse_system_channel_id`` works as intended.
    """
    system_channel_id = 202306150000
    
    for input_data, expected_output in (
        ({}, 0),
        ({'system_channel_id': None}, 0),
        ({'system_channel_id': str(system_channel_id)}, system_channel_id),
    ):
        output = parse_system_channel_id(input_data)
        vampytest.assert_eq(output, expected_output)
