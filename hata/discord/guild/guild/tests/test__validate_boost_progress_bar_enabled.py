import vampytest

from ..fields import validate_boost_progress_bar_enabled


def test__validate_boost_progress_bar_enabled__0():
    """
    Tests whether `validate_boost_progress_bar_enabled` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, False),
        (True, True),
        (False, False)
    ):
        output = validate_boost_progress_bar_enabled(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_boost_progress_bar_enabled__1():
    """
    Tests whether `validate_boost_progress_bar_enabled` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_boost_progress_bar_enabled(input_value)
