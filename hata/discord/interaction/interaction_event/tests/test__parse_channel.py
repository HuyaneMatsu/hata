import vampytest

from ....channel import Channel, ChannelType, create_partial_channel_from_id

from ..fields import parse_channel


def test__parse_channel():
    """
    Tests whether ``parse_channel`` works as intended.
    """
    channel_id = 202301150015
    channel = Channel.precreate(channel_id)
    
    default_channel = create_partial_channel_from_id(0, ChannelType.unknown, 0)
    
    
    for input_data, expected_output in (
        ({}, default_channel),
        ({'channel': None}, default_channel),
        ({'channel': {'id': str(channel_id)}}, channel),
    ):
        output = parse_channel(input_data)
        vampytest.assert_is(output, expected_output)
