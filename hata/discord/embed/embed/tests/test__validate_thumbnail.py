import vampytest

from ...embed_thumbnail import EmbedThumbnail

from ..fields import validate_thumbnail


def test__validate_thumbnail__0():
    """
    Tests whether `validate_thumbnail` works as intended.
    
    Case: passing.
    """
    thumbnail = EmbedThumbnail(url = 'https://orindance.party/')
    
    for input_value, expected_output in (
        (None, None),
        (thumbnail, thumbnail),
    ):
        output = validate_thumbnail(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_thumbnail__1():
    """
    Tests whether `validate_thumbnail` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_thumbnail(input_value)
