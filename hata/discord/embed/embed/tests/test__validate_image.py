import vampytest

from ...embed_image import EmbedImage

from ..fields import validate_image


def test__validate_image__0():
    """
    Tests whether `validate_image` works as intended.
    
    Case: passing.
    """
    image = EmbedImage(url = 'https://orindance.party/')
    
    for input_value, expected_output in (
        (None, None),
        (image, image),
    ):
        output = validate_image(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_image__1():
    """
    Tests whether `validate_image` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_image(input_value)
