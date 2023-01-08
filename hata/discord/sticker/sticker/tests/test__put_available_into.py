import vampytest

from ..fields import put_available_into


def test__put_available_into():
    """
    Tests whether ``put_available_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (True, False, {}),
        (True, True, {'available': True}),
        (False, False, {'available': False}),
    ):
        data = put_available_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
