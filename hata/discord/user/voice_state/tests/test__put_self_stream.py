import vampytest

from ..fields import put_self_stream


def test__put_self_stream():
    """
    Tests whether ``put_self_stream`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'self_stream': False}),
        (True, False, {'self_stream': True}),
    ):
        data = put_self_stream(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
