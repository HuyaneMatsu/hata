import vampytest

from ..video import EmbedVideo

from .test__EmbedVideo__constructor import _assert_fields_set


def test__EmbedVideo__from_data():
    """
    Tests whether ``EmbedVideo.from_data`` works as intended.
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
    
    embed_video = EmbedVideo.from_data(data)
    _assert_fields_set(embed_video)
    
    vampytest.assert_eq(embed_video.height, height)
    vampytest.assert_eq(embed_video.proxy_url, proxy_url)
    vampytest.assert_eq(embed_video.url, url)
    vampytest.assert_eq(embed_video.width, width)


def test__EmbedVideo__to_data():
    """
    Tests whether ``EmbedVideo.to_data`` works as intended.
    
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
    embed_video = EmbedVideo.from_data(data)
    
    expected_output = data
    
    vampytest.assert_eq(
        embed_video.to_data(defaults = True, include_internals = True),
        expected_output,
    )
