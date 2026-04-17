import vampytest

from ..fields import validate_matched_keyword


def test__validate_matched_keyword__0():
    """
    Tests whether `validate_matched_keyword` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_matched_keyword(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_matched_keyword__1():
    """
    Tests whether `validate_matched_keyword` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_matched_keyword(input_value)
