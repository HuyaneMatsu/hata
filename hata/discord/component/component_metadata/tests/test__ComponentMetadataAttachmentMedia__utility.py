import vampytest

from ....guild import Guild

from ...media_info import MediaInfo

from ..attachment_media import ComponentMetadataAttachmentMedia

from .test__ComponentMetadataAttachmentMedia__constructor import _assert_fields_set


def test__ComponentMetadataAttachmentMedia__clean_copy():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.clean_copy`` works as intended.
    """
    guild_id = 202505030012
    guild = Guild.precreate(guild_id)
    
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = media,
        spoiler = spoiler,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataAttachmentMedia__copy():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.copy`` works as intended.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = media,
        spoiler = spoiler,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)
    

def test__ComponentMetadataAttachmentMedia__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.copy_with`` works as intended.
    
    Case: No fields given.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = media,
        spoiler = spoiler,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataAttachmentMedia__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_media = MediaInfo('attachment://big_braids_orin.png')
    old_spoiler = True
    
    new_media = MediaInfo('attachment://orin.png')
    new_spoiler = False
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = old_media,
        spoiler = old_spoiler,
    )
    copy = component_metadata.copy_with(
        media = new_media,
        spoiler = new_spoiler,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_ne(copy, component_metadata)
    
    vampytest.assert_eq(copy.media, new_media)
    vampytest.assert_eq(copy.spoiler, new_spoiler)


def test__ComponentMetadataAttachmentMedia__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = media,
        spoiler = spoiler,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataAttachmentMedia__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    old_media = MediaInfo('attachment://big_braids_orin.png')
    old_spoiler = True
    
    new_media = MediaInfo('attachment://orin.png')
    new_spoiler = False
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = old_media,
        spoiler = old_spoiler,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'media': new_media,
        'spoiler': new_spoiler,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_ne(copy, component_metadata)
    
    vampytest.assert_eq(copy.media, new_media)
    vampytest.assert_eq(copy.spoiler, new_spoiler)


def _iter_options__iter_contents():
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'media': media,
            'spoiler': spoiler,
        },
        [],
    )

@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataAttachmentMedia__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataAttachmentMedia.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataAttachmentMedia(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
