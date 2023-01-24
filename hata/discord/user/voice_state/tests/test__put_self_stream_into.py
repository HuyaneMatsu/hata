import vampytest

from ..fields import put_self_stream_into


def test__put_self_stream_into():
    """
    Tests whether ``put_self_stream_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'self_stream': False}),
        (True, False, {'self_stream': True}),
    ):
        data = put_self_stream_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
