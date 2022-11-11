import vampytest

from ....channel import Channel, ChannelType

from ...interaction_event import InteractionEvent

from ..fields import parse_channels


def test__parse_channels():
    """
    Tests whether ``parse_channels`` works as intended.
    """
    channel_id = 202211050011
    guild_id = 202211050012
    channel_name = 'Faker'
    
    interaction_event = InteractionEvent(guild_id = guild_id)
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        name = channel_name,
    )
    
    for input_value, expected_output in (
        ({}, None),
        ({'channels': {}}, None),
        (
            {
                'channels': {
                    str(channel_id): channel.to_data(defaults = True, include_internals = True),
                }
            },
            {
                channel_id: channel,
            }
        )
    ):
        output = parse_channels(input_value, interaction_event)
        vampytest.assert_eq(output, expected_output)
