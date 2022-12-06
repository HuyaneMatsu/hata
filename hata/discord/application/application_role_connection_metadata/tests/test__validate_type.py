import vampytest

from ..fields import validate_type
from ..preinstanced import ApplicationRoleConnectionMetadataType


def test__validate_type__0():
    """
    Tests whether `validate_type` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (
            ApplicationRoleConnectionMetadataType.integer_equal,
            ApplicationRoleConnectionMetadataType.integer_equal,
        ),
        (
            ApplicationRoleConnectionMetadataType.integer_equal.value,
            ApplicationRoleConnectionMetadataType.integer_equal,
        )
    ):
        output = validate_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_type__1():
    """
    Tests whether `validate_type` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_type(input_value)
