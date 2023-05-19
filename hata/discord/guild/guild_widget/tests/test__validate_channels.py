import vampytest

from ...guild_widget_channel import GuildWidgetChannel

from ..fields import validate_channels


def test__validate_channels__0():
    """
    Validates whether ``validate_channels`` works as intended.
    
    Case: passing.
    """
    channel_id_0 = 202305190007
    channel_id_1 = 202305190008
    
    channel_0 = GuildWidgetChannel(channel_id = channel_id_0)
    channel_1 = GuildWidgetChannel(channel_id = channel_id_1)
    
    for input_value, expected_output in (
        ([], None),
        ([channel_0], (channel_0,)),
        ([channel_1, channel_0], (channel_0, channel_1)),
    ):
        output = validate_channels(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_channels__1():
    """
    Validates whether ``validate_channels`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_channels(input_value)
