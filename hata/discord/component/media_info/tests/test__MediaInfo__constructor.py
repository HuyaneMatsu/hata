import vampytest

from ..media_info import MediaInfo


def _assert_fields_set(media_info):
    """
    Checks whether the media info has every of its fields set.
    
    Parameters
    ----------
    media_info : ``MediaInfo``
        The media info to check.
    """
    vampytest.assert_instance(media_info, MediaInfo)
    vampytest.assert_instance(media_info.attachment_id, int)
    vampytest.assert_instance(media_info.content_type, str, nullable = True)
    vampytest.assert_instance(media_info.height, int)
    vampytest.assert_instance(media_info.proxy_url, str, nullable = True)
    vampytest.assert_instance(media_info.url, str)
    vampytest.assert_instance(media_info.width, int)


def test__MediaInfo__new():
    """
    Tests whether ``MediaInfo.__new__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    media_info = MediaInfo(url)
    _assert_fields_set(media_info)
    
    vampytest.assert_eq(media_info.url, url)


def test__MediaInfo__create_empty():
    """
    Tests whether ``MediaInfo._create_empty`` works as intended.
    
    Case: No fields given.
    """
    media_info = MediaInfo._create_empty()
    _assert_fields_set(media_info)


def test__MediaInfo__precreate__no_fields():
    """
    Tests whether ``MediaInfo.precreate`` works as intended.
    
    Case: No fields given.
    """
    media_info = MediaInfo.precreate()
    _assert_fields_set(media_info)


def test__MediaInfo__precreate__all_fields():
    """
    Tests whether ``MediaInfo.precreate`` works as intended.
    
    Case: No fields given.
    """
    attachment_id = 202509200004
    content_type = 'image/png'
    height = 56
    proxy_url = 'https://orindance.party/proxy'
    url = 'https://orindance.party/'
    width = 25
    
    media_info = MediaInfo.precreate(
        attachment_id = attachment_id,
        content_type = content_type,
        height = height,
        proxy_url = proxy_url,
        url = url,
        width = width,
    )
    _assert_fields_set(media_info)
    
    vampytest.assert_eq(media_info.attachment_id, attachment_id)
    vampytest.assert_eq(media_info.content_type, content_type)
    vampytest.assert_eq(media_info.height, height)
    vampytest.assert_eq(media_info.proxy_url, proxy_url)
    vampytest.assert_eq(media_info.url, url)
    vampytest.assert_eq(media_info.width, width)
