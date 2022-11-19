import vampytest

from ..fields import validate_regex_patterns


def test__validate_regex_patterns__0():
    """
    Tests whether `validate_regex_patterns` works as intended.
    
    Case: passing.
    """
    for input_regex_patterns, expected_output in (
        (None, None),
        ([], None),
        ('a', ('a',)),
        (['a'], ('a', )),
    ):
        output = validate_regex_patterns(input_regex_patterns)
        vampytest.assert_eq(output, expected_output)


def test__validate_regex_patterns__1():
    """
    Tests whether `validate_regex_patterns` works as intended.
    
    Case: `TypeError`.
    """
    for input_regex_patterns in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_regex_patterns(input_regex_patterns)
