import vampytest

from ..fields import put_type_into
from ..preinstanced import VerificationScreenStepType


def test__put_type_into():
    """
    Tests whether ``put_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (VerificationScreenStepType.rules, False, {'field_type': VerificationScreenStepType.rules.value}),
    ):
        data = put_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
