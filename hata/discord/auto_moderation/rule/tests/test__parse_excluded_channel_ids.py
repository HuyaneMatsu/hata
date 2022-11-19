import vampytest

from ..fields import parse_excluded_channel_ids


def test__parse_excluded_channel_ids():
    """
    Tests whether ``parse_excluded_channel_ids`` works as intended.
    """
    channel_id_1 = 202211170032
    channel_id_2 = 202211170033
    
    for input_data, expected_output in (
        ({}, None),
        ({'exempt_channels': None}, None),
        ({'exempt_channels': []}, None),
        ({'exempt_channels': [str(channel_id_1), str(channel_id_2)]}, (channel_id_1, channel_id_2)),
        ({'exempt_channels': [str(channel_id_2), str(channel_id_1)]}, (channel_id_1, channel_id_2)),
    ):
        output = parse_excluded_channel_ids(input_data)
        vampytest.assert_eq(output, expected_output)
