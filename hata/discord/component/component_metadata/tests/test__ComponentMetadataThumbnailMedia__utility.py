import vampytest

from ....guild import Guild

from ...media_info import MediaInfo

from ..thumbnail_media import ComponentMetadataThumbnailMedia

from .test__ComponentMetadataThumbnailMedia__constructor import _assert_fields_set


def test__ComponentMetadataThumbnailMedia__clean_copy():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.clean_copy`` works as intended.
    """
    guild_id = 202505030032
    guild = Guild.precreate(guild_id)
    
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = description,
        media = media,
        spoiler = spoiler,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataThumbnailMedia__copy():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.copy`` works as intended.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = description,
        media = media,
        spoiler = spoiler,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)
    

def test__ComponentMetadataThumbnailMedia__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.copy_with`` works as intended.
    
    Case: No fields given.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = description,
        media = media,
        spoiler = spoiler,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataThumbnailMedia__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_description = 'Its Orin <3'
    old_media = MediaInfo('attachment://big_braids_orin.png')
    old_spoiler = True
    
    new_description = 'Its Orin <3'
    new_media = MediaInfo('attachment://orin.png')
    new_spoiler = False
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = old_description,
        media = old_media,
        spoiler = old_spoiler,
    )
    copy = component_metadata.copy_with(
        description = new_description,
        media = new_media,
        spoiler = new_spoiler,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_ne(copy, component_metadata)
    
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.media, new_media)
    vampytest.assert_eq(copy.spoiler, new_spoiler)


def test__ComponentMetadataThumbnailMedia__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = description,
        media = media,
        spoiler = spoiler,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataThumbnailMedia__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    old_description = 'Its Orin <3'
    old_media = MediaInfo('attachment://big_braids_orin.png')
    old_spoiler = True
    
    new_description = 'Its Orin <3'
    new_media = MediaInfo('attachment://orin.png')
    new_spoiler = False
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = old_description,
        media = old_media,
        spoiler = old_spoiler,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'description': new_description,
        'media': new_media,
        'spoiler': new_spoiler,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_ne(copy, component_metadata)
    
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.media, new_media)
    vampytest.assert_eq(copy.spoiler, new_spoiler)


def _iter_options__iter_contents():
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'description': description,
            'media': media,
            'spoiler': spoiler,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataThumbnailMedia__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataThumbnailMedia.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataThumbnailMedia(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
