import vampytest

from ..fields import put_email_verified_into


def test__put_email_verified_into():
    """
    Tests whether ``put_email_verified_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'verified': False}),
        (True, False, {'verified': True}),
    ):
        data = put_email_verified_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
