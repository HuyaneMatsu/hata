import vampytest

from ....channel import Channel, ChannelType

from ..fields import put_channels_into


def test__put_channels_into():
    """
    Tests whether ``put_channels_into`` works as intended.
    """
    channel_id = 202211050013
    channel_name = 'Faker'
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        name = channel_name,
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'channels': {}}),
        (
            {
                channel_id: channel,
            },
                True,
            {
                'channels': {
                    str(channel_id): channel.to_data(defaults = True, include_internals = True),
                }
            },
        )
    ):
        output = put_channels_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
