import vampytest

from ..fields import validate_widget_enabled


def test__validate_widget_enabled__0():
    """
    Tests whether `validate_widget_enabled` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, False),
        (True, True),
        (False, False)
    ):
        output = validate_widget_enabled(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_widget_enabled__1():
    """
    Tests whether `validate_widget_enabled` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_widget_enabled(input_value)
