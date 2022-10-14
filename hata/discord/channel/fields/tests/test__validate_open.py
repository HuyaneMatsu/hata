import vampytest

from ..open_ import validate_open


def test__validate_open__0():
    """
    Tests whether `validate_open` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_open(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_open__1():
    """
    Tests whether `validate_open` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_open(input_value)
