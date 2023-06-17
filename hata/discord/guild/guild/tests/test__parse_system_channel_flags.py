import vampytest

from ..fields import parse_system_channel_flags
from ..flags import SystemChannelFlag


def test__parse_system_channel_flags():
    """
    Tests whether ``parse_system_channel_flags`` works as intended.
    """
    for input_data, expected_output in (
        ({}, SystemChannelFlag.NONE),
        ({'system_channel_flags': 1}, SystemChannelFlag(1)),
    ):
        output = parse_system_channel_flags(input_data)
        vampytest.assert_instance(output, SystemChannelFlag)
        vampytest.assert_eq(output, expected_output)
