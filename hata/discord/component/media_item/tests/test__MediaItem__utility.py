import vampytest

from ..media_item import MediaItem

from .test__MediaItem__constructor import _assert_fields_set


def test__MediaItem__copy():
    """
    Tests whether ``MediaItem.copy`` works as intended.
    """
    description = 'orin'
    spoiler = True
    url = 'https://orindance.party/'
    
    media_item = MediaItem(
        description = description,
        spoiler = spoiler,
        url = url,
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
    spoiler = True
    url = 'https://orindance.party/'
    
    media_item = MediaItem(
        description = description,
        spoiler = spoiler,
        url = url,
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
    old_spoiler = True
    old_url = 'https://orindance.party/'
    
    new_description = 'rin'
    new_spoiler = False
    new_url = 'https://www.astil.dev/'
    
    media_item = MediaItem(
        description = old_description,
        spoiler = old_spoiler,
        url = old_url,
    )
    copy = media_item.copy_with(
        description = new_description,
        spoiler = new_spoiler,
        url = new_url,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(media_item, copy)
    
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.spoiler, new_spoiler)
    vampytest.assert_eq(copy.url, new_url)
