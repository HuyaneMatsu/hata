import vampytest

from ..fields import validate_aliases


def test__validate_aliases__0():
    """
    Tests whether `validate_aliases` works as intended.
    
    Case: passing.
    """
    for input_aliases, expected_output in (
        (None, None),
        ([], None),
        ('a', ('a',)),
        (['a'], ('a', )),
    ):
        output = validate_aliases(input_aliases)
        vampytest.assert_eq(output, expected_output)


def test__validate_aliases__1():
    """
    Tests whether `validate_aliases` works as intended.
    
    Case: `TypeError`.
    """
    for input_aliases in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_aliases(input_aliases)
