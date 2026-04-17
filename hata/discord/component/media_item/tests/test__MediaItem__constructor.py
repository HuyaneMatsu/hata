import vampytest

from ...media_info import MediaInfo

from ..media_item import MediaItem


def _assert_fields_set(media_item):
    """
    Checks whether the media item has every of its fields set.
    
    Parameters
    ----------
    media_item : ``MediaItem``
        The media item to check.
    """
    vampytest.assert_instance(media_item, MediaItem)
    vampytest.assert_instance(media_item.description, str, nullable = True)
    vampytest.assert_instance(media_item.media, MediaInfo)
    vampytest.assert_instance(media_item.spoiler, bool)


def test__MediaItem__new__no_fields():
    """
    Tests whether ``MediaItem.__new__`` works as intended.
    
    Case: No fields given.
    """
    media = MediaInfo('https://orindance.party/')
    
    media_item = MediaItem(media)
    _assert_fields_set(media_item)
    
    vampytest.assert_eq(media_item.media, media)


def test__MediaItem__new__all_fields():
    """
    Tests whether ``MediaItem.__new__`` works as intended.
    
    Case: All fields given.
    """
    description = 'orin'
    media = MediaInfo('https://orindance.party/')
    spoiler = True
    
    media_item = MediaItem(
        media,
        description = description,
        spoiler = spoiler,
    )
    _assert_fields_set(media_item)
    
    vampytest.assert_eq(media_item.description, description)
    vampytest.assert_eq(media_item.media, media)
    vampytest.assert_eq(media_item.spoiler, spoiler)
