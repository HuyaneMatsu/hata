import vampytest

from ..fields import parse_public_updates_channel_id


def test__parse_public_updates_channel_id():
    """
    Tests whether ``parse_public_updates_channel_id`` works as intended.
    """
    public_updates_channel_id = 202306100005
    
    for input_data, expected_output in (
        ({}, 0),
        ({'public_updates_channel_id': None}, 0),
        ({'public_updates_channel_id': str(public_updates_channel_id)}, public_updates_channel_id),
    ):
        output = parse_public_updates_channel_id(input_data)
        vampytest.assert_eq(output, expected_output)
