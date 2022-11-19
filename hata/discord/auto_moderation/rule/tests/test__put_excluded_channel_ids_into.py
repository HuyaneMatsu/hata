import vampytest

from ..fields import put_excluded_channel_ids_into


def test__put_excluded_channel_ids_into():
    """
    Tests whether ``put_excluded_channel_ids_into`` is working as intended.
    """
    channel_id = 202211170036
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'exempt_channels': []}),
        ((channel_id, ), False, {'exempt_channels': [str(channel_id)]}),
    ):
        data = put_excluded_channel_ids_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
