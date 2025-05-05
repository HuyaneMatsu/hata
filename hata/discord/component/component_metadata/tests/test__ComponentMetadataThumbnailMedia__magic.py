import vampytest

from ...media_info import MediaInfo

from ..thumbnail_media import ComponentMetadataThumbnailMedia


def test__ComponentMetadataThumbnailMedia__repr():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.__repr__`` works as intended.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = description,
        media = media,
        spoiler = spoiler,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataThumbnailMedia__hash():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.__hash__`` works as intended.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = description,
        media = media,
        spoiler = spoiler,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataThumbnailMedia__eq__different_type():
    """
    Tests whether ``ComponentMetadataThumbnailMedia.__eq__`` works as intended.
    
    Case: different type.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataThumbnailMedia(
        description = description,
        media = media,
        spoiler = spoiler,
    )
    
    vampytest.assert_ne(component_metadata, object())


def _iter_options__eq():
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    keyword_parameters = {
        'description': description,
        'media': media,
        'spoiler': spoiler,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'media': MediaInfo('attachment://orin.png'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'spoiler': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ComponentMetadataThumbnailMedia__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataThumbnailMedia.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create from.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance from.
    
    Returns
    -------
    output : `bool`
    """
    component_metadata_0 = ComponentMetadataThumbnailMedia(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataThumbnailMedia(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
