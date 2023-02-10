import vampytest

from ..fields import validate_http_debug_options


def test__validate_http_debug_options__0():
    """
    Tests whether `validate_http_debug_options` works as intended.
    
    Case: passing.
    """
    debug_option_0 = 'youkai'
    debug_option_1 = 'girl'
    
    for input_value, expected_output in (
        (None, None),
        (debug_option_0, {debug_option_0}),
        ([], None),
        ([debug_option_0], {debug_option_0}),
        ([debug_option_0, debug_option_1], {debug_option_0, debug_option_1}),
    ):
        output = validate_http_debug_options(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_http_debug_options__1():
    """
    Tests whether `validate_http_debug_options` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_http_debug_options(input_value)
