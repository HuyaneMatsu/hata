import vampytest

from ..fields import put_verification_level
from ..preinstanced import VerificationLevel


def test__put_verification_level():
    """
    Tests whether ``put_verification_level`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (VerificationLevel.medium, False, {'verification_level': VerificationLevel.medium.value}),
    ):
        data = put_verification_level(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
