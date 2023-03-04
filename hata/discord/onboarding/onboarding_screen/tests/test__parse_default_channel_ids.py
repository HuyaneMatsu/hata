import vampytest

from ..fields import parse_default_channel_ids


def test__parse_default_channel_ids():
    """
    Tests whether ``parse_default_channel_ids`` works as intended.
    """
    channel_id_1 = 202303040029
    channel_id_2 = 202303040030
    
    for input_data, expected_output in (
        ({}, None),
        ({'default_channel_ids': None}, None),
        ({'default_channel_ids': []}, None),
        ({'default_channel_ids': [str(channel_id_1), str(channel_id_2)]}, (channel_id_1, channel_id_2)),
        ({'default_channel_ids': [str(channel_id_2), str(channel_id_1)]}, (channel_id_1, channel_id_2)),
    ):
        output = parse_default_channel_ids(input_data)
        vampytest.assert_eq(output, expected_output)
