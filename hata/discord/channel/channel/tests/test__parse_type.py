import vampytest

from ..fields import parse_type
from ..preinstanced import ChannelType


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ChannelType.unknown),
        ({'type': ChannelType.guild_text.value}, ChannelType.guild_text),
    ):
        output = parse_type(input_data)
        vampytest.assert_is(output, expected_output)
