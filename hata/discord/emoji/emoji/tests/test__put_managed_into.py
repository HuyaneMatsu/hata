import vampytest

from ..fields import put_managed_into


def test__put_managed_into():
    """
    Tests whether ``put_managed_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'managed': False}),
        (True, False, {'managed': True}),
    ):
        data = put_managed_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
