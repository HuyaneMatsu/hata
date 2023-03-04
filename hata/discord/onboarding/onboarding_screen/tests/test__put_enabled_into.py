import vampytest

from ..fields import put_enabled_into


def test__put_enabled_into():
    """
    Tests whether ``put_enabled_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, True, {'enabled': False}),
        (True, True, {'enabled': True}),
        (False, False, {'enabled': False}),
        (True, False, {}),
    ):
        data = put_enabled_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
