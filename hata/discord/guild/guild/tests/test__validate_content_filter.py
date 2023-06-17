import vampytest

from ..fields import validate_content_filter
from ..preinstanced import ContentFilterLevel


def test__validate_content_filter__0():
    """
    Tests whether `validate_content_filter` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (ContentFilterLevel.no_role, ContentFilterLevel.no_role),
        (ContentFilterLevel.no_role.value, ContentFilterLevel.no_role)
    ):
        output = validate_content_filter(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_content_filter__1():
    """
    Tests whether `validate_content_filter` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_content_filter(input_value)
