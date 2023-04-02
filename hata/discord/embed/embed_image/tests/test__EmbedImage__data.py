import vampytest

from ..image import EmbedImage

from .test__EmbedImage__constructor import _assert_fields_set


def test__EmbedImage__from_data():
    """
    Tests whether ``EmbedImage.from_data`` works as intended.
    """
    height = 1000
    proxy_url = 'https://www.astil.dev/'
    url = 'https://orindance.party/'
    width = 1001
    
    data = {
        'height': height,
        'proxy_url': proxy_url,
        'url': url,
        'width': width,
    }
    
    field = EmbedImage.from_data(data)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.height, height)
    vampytest.assert_eq(field.proxy_url, proxy_url)
    vampytest.assert_eq(field.url, url)
    vampytest.assert_eq(field.width, width)


def test__EmbedImage__to_data():
    """
    Tests whether ``EmbedImage.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    height = 1000
    proxy_url = 'https://www.astil.dev/'
    url = 'https://orindance.party/'
    width = 1001
    
    data = {
        'height': height,
        'proxy_url': proxy_url,
        'url': url,
        'width': width,
    }
    
    # We cant set the internal fields with the constructor, so we use `.from_data` instead.
    field = EmbedImage.from_data(data)
    
    expected_output = data
    
    vampytest.assert_eq(
        field.to_data(defaults = True, include_internals = True),
        expected_output,
    )
