import vampytest

from ...guild_widget_channel import GuildWidgetChannel

from ..fields import put_channels_into


def test__put_channels_into():
    """
    Tests whether ``put_channels_into`` works as intended.
    """
    channel_id_0 = 202305190005
    channel_name_0 = 'Far'
    
    channel_id_1 = 202305190006
    channel_name_1 = 'East'
    
    channel_0 = GuildWidgetChannel(
        channel_id = channel_id_0,
        name = channel_name_0,
    )
    
    channel_1 = GuildWidgetChannel(
        channel_id = channel_id_1,
        name = channel_name_1,
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {'channels': []}),
        (None, True, {'channels': []}),
        (
            (channel_0, channel_1),
            False,
            {
                'channels': [
                    channel_0.to_data(defaults = False),
                    channel_1.to_data(defaults = False),
                ],
            },
        ),
        (
            (channel_0, channel_1),
            True,
            {
                'channels': [
                    channel_0.to_data(defaults = True),
                    channel_1.to_data(defaults = True),
                ],
            },
        ),
    ):
        output = put_channels_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
