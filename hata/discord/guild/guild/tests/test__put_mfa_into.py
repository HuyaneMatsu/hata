import vampytest

from ..fields import put_mfa_into
from ..preinstanced import MFA


def test__put_mfa_into():
    """
    Tests whether ``put_mfa_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (MFA.elevated, False, {'mfa_level': MFA.elevated.value}),
    ):
        data = put_mfa_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
