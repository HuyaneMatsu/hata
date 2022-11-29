import vampytest

from ..fields import validate_bot_require_code_grant


def test__validate_bot_require_code_grant__0():
    """
    Tests whether `validate_bot_require_code_grant` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_bot_require_code_grant(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_bot_require_code_grant__1():
    """
    Tests whether `validate_bot_require_code_grant` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_bot_require_code_grant(input_value)
