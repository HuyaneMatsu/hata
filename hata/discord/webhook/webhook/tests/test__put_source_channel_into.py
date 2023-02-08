import vampytest

from ...webhook_source_channel import WebhookSourceChannel

from ..fields import put_source_channel_into


def test__put_source_channel_into():
    """
    Tests whether ``put_source_channel_into`` works as intended.
    """
    channel = WebhookSourceChannel(
        channel_id = 202302020008,
        name = 'itori',
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'source_channel': None}),
        (channel, False, {'source_channel': channel.to_data(defaults = False)}),
        (channel, True, {'source_channel': channel.to_data(defaults = True)}),
    ):
        data = put_source_channel_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
