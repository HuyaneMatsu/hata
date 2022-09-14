import vampytest

from ...flags import ChannelFlag

from ..flags import put_flags_into


def test__put_flags_into():
    """
    Tests whether ``put_flags_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (ChannelFlag(0), False, {}),
        (ChannelFlag(0), True, {'flags': 0}),
        (ChannelFlag(1), False, {'flags': 1}),
    ):
        data = put_flags_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
