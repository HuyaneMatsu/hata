import vampytest

from ..media_info import MediaInfo

from .test__MediaInfo__constructor import _assert_fields_set


def test__MediaInfo__from_data():
    """
    Tests whether ``MediaInfo.from_data`` works as intended.
    """
    content_type = 'image/png'
    height = 56
    proxy_url = 'https://orindance.party/proxy'
    url = 'https://orindance.party/'
    width = 23
    
    data = {
        'content_type': content_type,
        'height': height,
        'proxy_url': proxy_url,
        'url': url,
        'width': width,
    }
    
    media_info = MediaInfo.from_data(data)
    _assert_fields_set(media_info)
    
    vampytest.assert_eq(media_info.content_type, content_type)
    vampytest.assert_eq(media_info.height, height)
    vampytest.assert_eq(media_info.proxy_url, proxy_url)
    vampytest.assert_eq(media_info.url, url)
    vampytest.assert_eq(media_info.width, width)


def test__MediaInfo__to_data():
    """
    Tests whether ``MediaInfo.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    content_type = 'image/png'
    height = 56
    proxy_url = 'https://orindance.party/proxy'
    url = 'https://orindance.party/'
    width = 23
    
    media_info = MediaInfo.precreate(
        content_type = content_type,
        height = height,
        proxy_url = proxy_url,
        url = url,
        width = width,
    )
    
    expected_output = {
        'content_type': content_type,
        'height': height,
        'proxy_url': proxy_url,
        'url': url,
        'width': width,
    }
    
    vampytest.assert_eq(
        media_info.to_data(defaults = True, include_internals = True),
        expected_output,
    )
