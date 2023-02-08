import vampytest

from ..fields import put_mfa_into


def test__put_mfa_into():
    """
    Tests whether ``put_mfa_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'mfa_enabled': False}),
        (True, False, {'mfa_enabled': True}),
    ):
        data = put_mfa_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
