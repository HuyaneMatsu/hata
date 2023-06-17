import vampytest

from ..fields import put_verification_level_into
from ..preinstanced import VerificationLevel


def test__put_verification_level_into():
    """
    Tests whether ``put_verification_level_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (VerificationLevel.medium, False, {'verification_level': VerificationLevel.medium.value}),
    ):
        data = put_verification_level_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
