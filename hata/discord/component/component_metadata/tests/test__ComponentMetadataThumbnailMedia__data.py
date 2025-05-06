import vampytest

from ...media_info import MediaInfo

from ..thumbnail_media import ComponentMetadataThumbnailMedia

from .test__ComponentMetadataThumbnailMedia__constructor import _assert_fields_set


def test__ComponentMetadataThumbnailMedia__from_data():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.from_data`` works as intended.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    data = {
        'description': description,
        'media': media.to_data(defaults = True, include_internals = True),
        'spoiler': spoiler,
    }
    
    component_metadata = ComponentMetadataThumbnailMedia.from_data(data)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.description, description)
    vampytest.assert_eq(component_metadata.media, media)
    vampytest.assert_eq(component_metadata.spoiler, spoiler)


def test__ComponentMetadataThumbnailMedia__to_data():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = description,
        media = media,
        spoiler = spoiler,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'description': description,
            'media': media.to_data(defaults = True, include_internals = True),
            'spoiler': spoiler,
        },
    )
