import vampytest

from ..fields import put_pending_into


def test__put_pending_into():
    """
    Tests whether ``put_pending_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'pending': False}),
        (True, False, {'pending': True}),
    ):
        data = put_pending_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
