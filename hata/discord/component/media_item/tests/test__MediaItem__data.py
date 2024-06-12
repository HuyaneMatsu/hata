import vampytest

from ..media_item import MediaItem

from .test__MediaItem__constructor import _assert_fields_set


def test__MediaItem__from_data():
    """
    Tests whether ``MediaItem.from_data`` works as intended.
    """
    description = 'orin'
    spoiler = True
    url = 'https://orindance.party/'
    
    data = {
        'description': description,
        'spoiler': spoiler,
        'url': url,
    }
    
    media_item = MediaItem.from_data(data)
    _assert_fields_set(media_item)
    
    vampytest.assert_eq(media_item.description, description)
    vampytest.assert_eq(media_item.spoiler, spoiler)
    vampytest.assert_eq(media_item.url, url)


def test__MediaItem__to_data():
    """
    Tests whether ``MediaItem.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    description = 'orin'
    spoiler = True
    url = 'https://orindance.party/'
    
    media_item = MediaItem(
        description = description,
        spoiler = spoiler,
        url = url,
    )
    
    expected_output = {
        'description': description,
        'spoiler': spoiler,
        'url': url,
    }
    
    vampytest.assert_eq(
        media_item.to_data(defaults = True),
        expected_output,
    )
