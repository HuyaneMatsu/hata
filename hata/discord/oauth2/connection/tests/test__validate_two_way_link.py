import vampytest

from ..fields import validate_two_way_link


def test__validate_two_way_link__0():
    """
    Tests whether `validate_two_way_link` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_two_way_link(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_two_way_link__1():
    """
    Tests whether `validate_two_way_link` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_two_way_link(input_value)
