import vampytest

from ....channel import ChannelType

from ..fields import put_channel_types


def test__put_channel_types():
    """
    Tests whether ``put_channel_types`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'channel_types': []}),
        ((ChannelType.private, ), True, {'channel_types': [ChannelType.private.value]}),
    ):
        data = put_channel_types(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
