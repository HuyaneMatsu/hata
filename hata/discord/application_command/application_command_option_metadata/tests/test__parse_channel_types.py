import vampytest

from ....channel import ChannelType

from ..fields import parse_channel_types


def test__parse_channel_types():
    """
    Tests whether ``parse_channel_types`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'channel_types': None}, None),
        ({'channel_types': []}, None),
        (
            {'channel_types': [ChannelType.guild_text.value, ChannelType.guild_forum.value]},
            (ChannelType.guild_text, ChannelType.guild_forum,),
        ),
    ):
        output = parse_channel_types(input_data)
        vampytest.assert_eq(output, expected_output)
