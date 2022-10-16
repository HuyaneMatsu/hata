import vampytest

from ...flags import ChannelFlag

from ..flags import parse_flags


def test__parse_flags():
    """
    Tests whether ``parse_flags`` works as intended."""
    for input_data, expected_output in (
        ({}, ChannelFlag(0)),
        ({'flags': 1}, ChannelFlag(1)),
    ):
        output = parse_flags(input_data)
        vampytest.assert_instance(output, ChannelFlag)
        vampytest.assert_eq(output, expected_output)
