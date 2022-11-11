import vampytest

from ..fields import put_channel_id_into


def test__put_channel_id_into():
    """
    Tests whether ``put_channel_id_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'channel_id': None}),
        (1, False, {'channel_id': '1'}),
    ):
        data = put_channel_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
