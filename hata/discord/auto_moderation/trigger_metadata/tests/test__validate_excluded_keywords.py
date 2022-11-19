import vampytest

from ..fields import validate_excluded_keywords


def test__validate_excluded_keywords__0():
    """
    Tests whether `validate_excluded_keywords` works as intended.
    
    Case: passing.
    """
    for input_excluded_keywords, expected_output in (
        (None, None),
        ([], None),
        ('a', ('a',)),
        (['a'], ('a', )),
    ):
        output = validate_excluded_keywords(input_excluded_keywords)
        vampytest.assert_eq(output, expected_output)


def test__validate_excluded_keywords__1():
    """
    Tests whether `validate_excluded_keywords` works as intended.
    
    Case: `TypeError`.
    """
    for input_excluded_keywords in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_excluded_keywords(input_excluded_keywords)
