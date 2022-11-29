import vampytest

from ..fields import validate_tags


def test__validate_tags__0():
    """
    Tests whether `validate_tags` works as intended.
    
    Case: passing.
    """
    for input_tags, expected_output in (
        (None, None),
        ([], None),
        ('a', ('a',)),
        (['a'], ('a', )),
    ):
        output = validate_tags(input_tags)
        vampytest.assert_eq(output, expected_output)


def test__validate_tags__1():
    """
    Tests whether `validate_tags` works as intended.
    
    Case: `TypeError`.
    """
    for input_tags in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_tags(input_tags)
