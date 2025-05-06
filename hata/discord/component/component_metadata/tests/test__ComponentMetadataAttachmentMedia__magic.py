import vampytest

from ...media_info import MediaInfo

from ..attachment_media import ComponentMetadataAttachmentMedia


def test__ComponentMetadataAttachmentMedia__repr():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.__repr__`` works as intended.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = media,
        spoiler = spoiler,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataAttachmentMedia__hash():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.__hash__`` works as intended.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = media,
        spoiler = spoiler,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataAttachmentMedia__eq__different_type():
    """
    Tests whether ``ComponentMetadataAttachmentMedia.__eq__`` works as intended.
    
    Case: different type.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component_metadata = ComponentMetadataAttachmentMedia(
        media = media,
        spoiler = spoiler,
    )
    
    vampytest.assert_ne(component_metadata, object())


def _iter_options__eq():
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    keyword_parameters = {
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


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ComponentMetadataAttachmentMedia__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataAttachmentMedia.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataAttachmentMedia(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataAttachmentMedia(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
