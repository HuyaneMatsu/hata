import vampytest

from ..fields import validate_format
from ..preinstanced import StickerFormat


def test__validate_format__0():
    """
    Validates whether ``validate_format`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (StickerFormat.png, StickerFormat.png),
        (StickerFormat.png.value, StickerFormat.png),
    ):
        output = validate_format(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_format__1():
    """
    Validates whether ``validate_format`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_format(input_value)
