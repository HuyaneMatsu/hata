import vampytest

from ...embed_footer import EmbedFooter

from ..fields import validate_footer


def test__validate_footer__0():
    """
    Tests whether `validate_footer` works as intended.
    
    Case: passing.
    """
    footer = EmbedFooter(text = 'hell')
    
    for input_value, expected_output in (
        (None, None),
        (footer, footer),
    ):
        output = validate_footer(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_footer__1():
    """
    Tests whether `validate_footer` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_footer(input_value)
