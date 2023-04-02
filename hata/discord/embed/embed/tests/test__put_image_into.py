import vampytest

from ...embed_image import EmbedImage

from ..fields import put_image_into


def test__put_image_into():
    """
    Tests whether ``put_image_into`` is working as intended.
    """
    image = EmbedImage(url = 'https://orindance.party/')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (image, False, {'image': image.to_data()}),
        (image, True, {'image': image.to_data(defaults = True)}),
    ):
        data = put_image_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
