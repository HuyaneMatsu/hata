import vampytest

from ..fields import validate_overlay_compatibility_hook


def test__validate_overlay_compatibility_hook__0():
    """
    Tests whether `validate_overlay_compatibility_hook` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_overlay_compatibility_hook(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_overlay_compatibility_hook__1():
    """
    Tests whether `validate_overlay_compatibility_hook` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_overlay_compatibility_hook(input_value)
