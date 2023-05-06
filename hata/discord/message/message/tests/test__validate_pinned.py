import vampytest

from ..fields import validate_pinned


def test__validate_pinned__0():
    """
    Tests whether `validate_pinned` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_pinned(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_pinned__1():
    """
    Tests whether `validate_pinned` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_pinned(input_value)
