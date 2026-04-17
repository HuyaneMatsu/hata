import vampytest

from ...media_info import MediaInfo

from ..media_item import MediaItem

from .test__MediaItem__constructor import _assert_fields_set


def test__MediaItem__from_data():
    """
    Tests whether ``MediaItem.from_data`` works as intended.
    """
    description = 'orin'
    media = MediaInfo('https://orindance.party/')
    spoiler = True
    
    data = {
        'description': description,
        'media': media.to_data(include_internals = True),
        'spoiler': spoiler,
    }
    
    media_item = MediaItem.from_data(data)
    _assert_fields_set(media_item)
    
    vampytest.assert_eq(media_item.description, description)
    vampytest.assert_eq(media_item.media, media)
    vampytest.assert_eq(media_item.spoiler, spoiler)


def test__MediaItem__to_data():
    """
    Tests whether ``MediaItem.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    description = 'orin'
    media = MediaInfo('https://orindance.party/')
    spoiler = True
    
    media_item = MediaItem(
        media,
        description = description,
        spoiler = spoiler,
    )
    
    expected_output = {
        'description': description,
        'media': media.to_data(defaults = True, include_internals = True),
        'spoiler': spoiler,
    }
    
    vampytest.assert_eq(
        media_item.to_data(defaults = True, include_internals = True),
        expected_output,
    )
