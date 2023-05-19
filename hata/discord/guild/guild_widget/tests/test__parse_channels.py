import vampytest

from ...guild_widget_channel import GuildWidgetChannel

from ..fields import parse_channels


def test__parse_channels():
    """
    Tests whether ``parse_channels`` works as intended.
    """
    channel_id_0 = 202305190003
    channel_name_0 = 'Far'
    
    channel_id_1 = 202305190004
    channel_name_1 = 'East'
    
    channel_0 = GuildWidgetChannel(
        channel_id = channel_id_0,
        name = channel_name_0,
    )
    
    channel_1 = GuildWidgetChannel(
        channel_id = channel_id_1,
        name = channel_name_1,
    )
    
    for input_data, expected_output in (
        ({}, None),
        ({'channels': None}, None),
        ({'channels': []}, None),
        (
            {
                'channels': [
                    channel_0.to_data(),
                ],
            },
            (channel_0,),
        ),
        (
            {
                'channels': [
                    channel_0.to_data(),
                    channel_1.to_data(),
                ],
            },
            (channel_0, channel_1),
        ),
    ):
        output = parse_channels(input_data)
        vampytest.assert_eq(output, expected_output)
