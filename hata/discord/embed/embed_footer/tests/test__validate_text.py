import vampytest

from ..constants import EMBED_FOOTER_TEXT_LENGTH_MAX
from ..fields import validate_text


def test__validate_text__0():
    """
    Tests whether `validate_text` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
        (1, '1'),
    ):
        output = validate_text(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_text__1():
    """
    Tests whether `validate_text` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (EMBED_FOOTER_TEXT_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_text(input_value)
