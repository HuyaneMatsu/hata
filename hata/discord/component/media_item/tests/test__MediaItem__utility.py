import vampytest

from ...media_info import MediaInfo

from ..media_item import MediaItem

from .test__MediaItem__constructor import _assert_fields_set


def test__MediaItem__copy():
    """
    Tests whether ``MediaItem.copy`` works as intended.
    """
    description = 'orin'
    media = MediaInfo('https://orindance.party/')
    spoiler = True
    
    media_item = MediaItem(
        media,
        description = description,
        spoiler = spoiler,
    )
    copy = media_item.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(media_item, copy)
    
    vampytest.assert_eq(media_item, copy)


def test__MediaItem__copy_with__no_fields():
    """
    Tests whether ``MediaItem.copy_with`` works as intended.
    
    Case: No fields given.
    """
    description = 'orin'
    media = MediaInfo('https://orindance.party/')
    spoiler = True
    
    media_item = MediaItem(
        media,
        description = description,
        spoiler = spoiler,
    )
    copy = media_item.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(media_item, copy)
    
    vampytest.assert_eq(media_item, copy)


def test__MediaItem__copy_with__all_fields():
    """
    Tests whether ``MediaItem.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_description = 'orin'
    old_media = MediaInfo('https://orindance.party/')
    old_spoiler = True
    
    new_description = 'rin'
    new_media = MediaInfo('https://www.astil.dev/')
    new_spoiler = False
    
    media_item = MediaItem(
        old_media,
        description = old_description,
        spoiler = old_spoiler,
    )
    copy = media_item.copy_with(
        description = new_description,
        media = new_media,
        spoiler = new_spoiler,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(media_item, copy)
    
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.media, new_media)
    vampytest.assert_eq(copy.spoiler, new_spoiler)


def test__MediaItem__url():
    """
    Tests whether ``MediaItem.url`` works as intended.
    """
    url = 'https://orindance.party/'
    
    media_item = MediaItem(MediaInfo(url))
    
    output = media_item.url
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, url)
