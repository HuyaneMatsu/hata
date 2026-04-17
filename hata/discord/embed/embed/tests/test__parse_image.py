import vampytest

from ...embed_image import EmbedImage

from ..fields import parse_image


def test__parse_image():
    """
    Tests whether ``parse_image`` works as intended.
    """
    image = EmbedImage(url = 'https://orindance.party/')
    
    for input_data, expected_output in (
        ({}, None),
        ({'image': None}, None),
        ({'image': image.to_data()}, image),
    ):
        output = parse_image(input_data)
        vampytest.assert_eq(output, expected_output)
