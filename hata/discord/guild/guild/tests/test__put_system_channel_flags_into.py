import vampytest

from ..fields import put_system_channel_flags_into
from ..flags import SystemChannelFlag


def test__put_system_channel_flags_into():
    """
    Tests whether ``put_system_channel_flags_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (SystemChannelFlag(0), False, {'system_channel_flags': 0}),
        (SystemChannelFlag(0), True, {'system_channel_flags': 0}),
        (SystemChannelFlag(1), False, {'system_channel_flags': 1}),
    ):
        data = put_system_channel_flags_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
