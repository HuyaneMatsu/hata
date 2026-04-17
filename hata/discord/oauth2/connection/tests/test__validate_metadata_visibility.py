import vampytest

from ..fields import validate_metadata_visibility
from ..preinstanced import ConnectionVisibility


def test__validate_metadata_visibility__0():
    """
    Tests whether `validate_metadata_visibility` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (ConnectionVisibility.user_only, ConnectionVisibility.user_only),
        (ConnectionVisibility.user_only.value, ConnectionVisibility.user_only)
    ):
        output = validate_metadata_visibility(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_metadata_visibility__1():
    """
    Tests whether `validate_metadata_visibility` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_metadata_visibility(input_value)
