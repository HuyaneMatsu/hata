import vampytest

from ...embed_author import EmbedAuthor

from ..fields import validate_author


def test__validate_author__0():
    """
    Tests whether `validate_author` works as intended.
    
    Case: passing.
    """
    author = EmbedAuthor(name = 'hell')
    
    for input_value, expected_output in (
        (None, None),
        (author, author),
    ):
        output = validate_author(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_author__1():
    """
    Tests whether `validate_author` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_author(input_value)
