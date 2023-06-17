import vampytest

from ..fields import parse_mfa
from ..preinstanced import MFA


def test__parse_mfa():
    """
    Tests whether ``parse_mfa`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MFA.none),
        ({'mfa_level': MFA.elevated.value}, MFA.elevated),
    ):
        output = parse_mfa(input_data)
        vampytest.assert_eq(output, expected_output)
