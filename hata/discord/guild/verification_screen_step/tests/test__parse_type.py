import vampytest

from ..fields import parse_type
from ..preinstanced import VerificationScreenStepType


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, VerificationScreenStepType.none),
        ({'field_type': VerificationScreenStepType.none.value}, VerificationScreenStepType.none),
        ({'field_type': VerificationScreenStepType.rules.value}, VerificationScreenStepType.rules),
    ):
        output = parse_type(input_data)
        vampytest.assert_eq(output, expected_output)
