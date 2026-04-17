import vampytest

from ..fields import put_available


def test__put_available():
    """
    Tests whether ``put_available`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (True, False, {}),
        (True, True, {'available': True}),
        (False, False, {'available': False}),
    ):
        data = put_available(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
