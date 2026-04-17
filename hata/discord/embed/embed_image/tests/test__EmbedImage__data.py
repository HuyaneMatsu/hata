import vampytest

from ...embed_field_base import EmbedMediaFlag

from ..image import EmbedImage

from .test__EmbedImage__constructor import _assert_fields_set


def test__EmbedImage__from_data():
    """
    Tests whether ``EmbedImage.from_data`` works as intended.
    """
    flags = EmbedMediaFlag(3)
    height = 1000
    proxy_url = 'https://www.astil.dev/'
    url = 'https://orindance.party/'
    width = 1001
    
    data = {
        'flags': flags,
        'height': height,
        'proxy_url': proxy_url,
        'url': url,
        'width': width,
    }
    
    embed_image = EmbedImage.from_data(data)
    _assert_fields_set(embed_image)
    
    vampytest.assert_eq(embed_image.flags, flags)
    vampytest.assert_eq(embed_image.height, height)
    vampytest.assert_eq(embed_image.proxy_url, proxy_url)
    vampytest.assert_eq(embed_image.url, url)
    vampytest.assert_eq(embed_image.width, width)


def test__EmbedImage__to_data():
    """
    Tests whether ``EmbedImage.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    flags = EmbedMediaFlag(3)
    height = 1000
    proxy_url = 'https://www.astil.dev/'
    url = 'https://orindance.party/'
    width = 1001
    
    data = {
        'flags': flags,
        'height': height,
        'proxy_url': proxy_url,
        'url': url,
        'width': width,
    }
    
    # We cant set the internal fields with the constructor, so we use `.from_data` instead.
    embed_image = EmbedImage.from_data(data)
    
    expected_output = data
    
    vampytest.assert_eq(
        embed_image.to_data(defaults = True, include_internals = True),
        expected_output,
    )
