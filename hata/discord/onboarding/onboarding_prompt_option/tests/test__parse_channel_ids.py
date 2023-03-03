import vampytest

from ..fields import parse_channel_ids


def test__parse_channel_ids():
    """
    Tests whether ``parse_channel_ids`` works as intended.
    """
    channel_id_1 = 202303030005
    channel_id_2 = 202303030006
    
    for input_data, expected_output in (
        ({}, None),
        ({'channel_ids': None}, None),
        ({'channel_ids': []}, None),
        ({'channel_ids': [str(channel_id_1), str(channel_id_2)]}, (channel_id_1, channel_id_2)),
        ({'channel_ids': [str(channel_id_2), str(channel_id_1)]}, (channel_id_1, channel_id_2)),
    ):
        output = parse_channel_ids(input_data)
        vampytest.assert_eq(output, expected_output)
