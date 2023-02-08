import vampytest

from ...webhook_source_channel import WebhookSourceChannel

from ..fields import parse_source_channel


def test__parse_source_channel():
    """
    Tests whether ``parse_source_channel`` works as intended. 
    """
    channel = WebhookSourceChannel(
        channel_id = 202302020006,
        name = 'itori',
    )
    
    for input_data, expected_output in (
        ({}, None),
        ({'source_channel': None}, None),
        ({'source_channel': channel.to_data(defaults = True)}, channel),
    ):
        output = parse_source_channel(input_data)
        vampytest.assert_eq(output, expected_output)
