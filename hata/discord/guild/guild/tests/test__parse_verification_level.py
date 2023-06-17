import vampytest

from ..fields import parse_verification_level
from ..preinstanced import VerificationLevel


def test__parse_verification_level():
    """
    Tests whether ``parse_verification_level`` works as intended.
    """
    for input_data, expected_output in (
        ({}, VerificationLevel.none),
        ({'verification_level': VerificationLevel.medium.value}, VerificationLevel.medium),
    ):
        output = parse_verification_level(input_data)
        vampytest.assert_eq(output, expected_output)
