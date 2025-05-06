import vampytest

from ..fields import put_channel_ids


def test__put_channel_ids():
    """
    Tests whether ``put_channel_ids`` is working as intended.
    """
    channel_id = 202303030002
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'channel_ids': []}),
        ((channel_id, ), False, {'channel_ids': [str(channel_id)]}),
    ):
        data = put_channel_ids(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
