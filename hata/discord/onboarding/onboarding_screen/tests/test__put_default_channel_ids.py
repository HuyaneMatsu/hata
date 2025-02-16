import vampytest

from ..fields import put_default_channel_ids


def test__put_default_channel_ids():
    """
    Tests whether ``put_default_channel_ids`` is working as intended.
    """
    channel_id = 202303040031
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'default_channel_ids': []}),
        ((channel_id, ), False, {'default_channel_ids': [str(channel_id)]}),
    ):
        data = put_default_channel_ids(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
