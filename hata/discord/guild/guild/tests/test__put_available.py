import vampytest

from ..fields import put_available


def test__put_available():
    """
    Tests whether ``put_available`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (True, False, {}),
        (True, True, {'unavailable': False}),
        (False, False, {'unavailable': True}),
    ):
        data = put_available(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
