import vampytest

from ..fields import validate_tags


def test__validate_tags__0():
    """
    Tests whether `validate_tags` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ('', None),
        ('lost', frozenset(('lost',))),
        ('lost, emotion', frozenset(('lost', 'emotion'))),
        (['lost'], frozenset(('lost',))),
        (['lost', 'emotion'], frozenset(('lost', 'emotion'))),
    ):
        output = validate_tags(input_value)
        vampytest.assert_eq(output, expected_output)



def test__validate_tags__1():
    """
    Tests whether `validate_tags` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_tags(input_value)
