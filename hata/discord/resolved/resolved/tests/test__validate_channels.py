import vampytest

from ....channel import Channel, ChannelType

from ..fields import validate_channels


def test__validate_channels__0():
    """
    Tests whether ``validate_channels`` works as intended.
    
    Case: passing.
    """
    channel_id = 202211050014
    channel_name = 'Faker'
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        name = channel_name,
    )
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ({}, None),
        ([channel], {channel_id: channel}),
        ({channel_id: channel}, {channel_id: channel}),
    ):
        output = validate_channels(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_channels__1():
    """
    Tests whether ``validate_channels`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_channels(input_value)
