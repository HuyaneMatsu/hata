import vampytest

from ....channel import ChannelType

from ..fields import put_channel_types_into


def test__put_channel_types_into():
    """
    Tests whether ``put_channel_types_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'channel_types': []}),
        ((ChannelType.private, ), True, {'channel_types': [ChannelType.private.value]}),
    ):
        data = put_channel_types_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
