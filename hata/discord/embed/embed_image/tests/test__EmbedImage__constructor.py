import vampytest

from ...embed_field_base import EmbedMediaFlag

from ..image import EmbedImage


def _assert_fields_set(embed_image):
    """
    Checks whether every fields of the given embed image are set.
    
    Parameters
    ----------
    embed_image : ``EmbedImage``
        The field to check.
    """
    vampytest.assert_instance(embed_image, EmbedImage)
    vampytest.assert_instance(embed_image.flags, EmbedMediaFlag)
    vampytest.assert_instance(embed_image.height, int)
    vampytest.assert_instance(embed_image.url, str, nullable = True)
    vampytest.assert_instance(embed_image.proxy_url, str, nullable = True)
    vampytest.assert_instance(embed_image.width, int)


def test__EmbedImage__new():
    """
    Tests whether ``EmbedImage.__new__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    embed_image = EmbedImage(url)
    _assert_fields_set(embed_image)
    
    vampytest.assert_eq(embed_image.url, url)
