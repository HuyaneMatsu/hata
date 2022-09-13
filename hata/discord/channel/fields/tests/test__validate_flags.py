import vampytest

from ...flags import ChannelFlag

from ..flags import validate_flags


def test__validate_flags():
    """
    Tests whether `validate_flags` works as intended.
    """
    for input_value, expected_output in (
        (1, ChannelFlag(1)),
        (ChannelFlag(1), ChannelFlag(1)),
    ):
        output = validate_flags(input_value)
        vampytest.assert_instance(output, ChannelFlag)
        vampytest.assert_eq(output, expected_output)
