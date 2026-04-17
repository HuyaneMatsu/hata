import vampytest

from ..fields import validate_archived


def test__validate_archived__0():
    """
    Tests whether `validate_archived` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_archived(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_archived__1():
    """
    Tests whether `validate_archived` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_archived(input_value)
