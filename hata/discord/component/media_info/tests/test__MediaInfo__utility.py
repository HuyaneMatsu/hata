import vampytest

from ..media_info import MediaInfo

from .test__MediaInfo__constructor import _assert_fields_set


def test__MediaInfo__copy():
    """
    Tests whether ``MediaInfo.copy`` works as intended.
    """
    url = 'https://orindance.party/'
    
    media_info = MediaInfo(url)
    copy = media_info.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(media_info, copy)
    
    vampytest.assert_eq(media_info, copy)


def test__MediaInfo__copy_with__no_fields():
    """
    Tests whether ``MediaInfo.copy_with`` works as intended.
    
    Case: No fields given.
    """
    url = 'https://orindance.party/'
    
    media_info = MediaInfo(url)
    copy = media_info.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(media_info, copy)
    
    vampytest.assert_eq(media_info, copy)


def test__MediaInfo__copy_with__all_fields():
    """
    Tests whether ``MediaInfo.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_url = 'https://orindance.party/'
    
    new_url = 'https://www.astil.dev/'
    
    media_info = MediaInfo(old_url)
    copy = media_info.copy_with(
        url = new_url,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(media_info, copy)
    
    vampytest.assert_eq(copy.url, new_url)
