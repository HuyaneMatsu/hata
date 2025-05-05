import vampytest

from ...media_info import MediaInfo

from ..attachment_media import ComponentMetadataAttachmentMedia

from .test__ComponentMetadataAttachmentMedia__constructor import _assert_fields_set


def test__ComponentMetadataAttachmentMedia__from_data():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.from_data`` works as intended.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    data = {
        'file': media.to_data(defaults = True, include_internals = True),
        'spoiler': spoiler,
    }
    
    component_metadata = ComponentMetadataAttachmentMedia.from_data(data)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.media, media)
    vampytest.assert_eq(component_metadata.spoiler, spoiler)


def test__ComponentMetadataAttachmentMedia__to_data():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = media,
        spoiler = spoiler,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'file': media.to_data(defaults = True, include_internals = True),
            'spoiler': spoiler,
        },
    )
