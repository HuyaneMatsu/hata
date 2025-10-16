import vampytest

from ...media_info import MediaInfo

from ..attachment_media import ComponentMetadataAttachmentMedia


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataAttachmentMedia`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataAttachmentMedia``
        Component metadata to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataAttachmentMedia)
    vampytest.assert_instance(component_metadata.media, MediaInfo)
    vampytest.assert_instance(component_metadata.name, str)
    vampytest.assert_instance(component_metadata.size, int)
    vampytest.assert_instance(component_metadata.spoiler, bool)


def test__ComponentMetadataAttachmentMedia__new__no_fields():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataAttachmentMedia()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataAttachmentMedia__new__all_fields():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.__new__`` works as intended.
    
    Case: all fields given.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = media,
        spoiler = spoiler,
    )
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.media, media)
    vampytest.assert_eq(component_metadata.spoiler, spoiler)


def test__ComponentMetadataAttachmentMedia__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataAttachmentMedia.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataAttachmentMedia__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    keyword_parameters = {
        'media': media,
        'spoiler': spoiler,
    }
    
    component_metadata = ComponentMetadataAttachmentMedia.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.media, media)
    vampytest.assert_eq(component_metadata.spoiler, spoiler)
