import vampytest

from ...media_info import MediaInfo

from ..thumbnail_media import ComponentMetadataThumbnailMedia


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataThumbnailMedia`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataThumbnailMedia``
        Component metadata to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataThumbnailMedia)
    vampytest.assert_instance(component_metadata.description, str, nullable = True)
    vampytest.assert_instance(component_metadata.media, MediaInfo)
    vampytest.assert_instance(component_metadata.spoiler, bool)


def test__ComponentMetadataThumbnailMedia__new__no_fields():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataThumbnailMedia()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataThumbnailMedia__new__all_fields():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.__new__`` works as intended.
    
    Case: all fields given.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = description,
        media = media,
        spoiler = spoiler,
    )
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.description, description)
    vampytest.assert_eq(component_metadata.media, media)
    vampytest.assert_eq(component_metadata.spoiler, spoiler)


def test__ComponentMetadataThumbnailMedia__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataThumbnailMedia.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataThumbnailMedia__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    keyword_parameters = {
        'description': description,
        'media': media,
        'spoiler': spoiler,
    }
    
    component_metadata = ComponentMetadataThumbnailMedia.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.description, description)
    vampytest.assert_eq(component_metadata.media, media)
    vampytest.assert_eq(component_metadata.spoiler, spoiler)
