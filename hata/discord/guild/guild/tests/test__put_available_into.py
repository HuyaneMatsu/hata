import vampytest

from ..fields import put_available_into


def test__put_available_into():
    """
    Tests whether ``put_available_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (True, False, {}),
        (True, True, {'unavailable': False}),
        (False, False, {'unavailable': True}),
    ):
        data = put_available_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
