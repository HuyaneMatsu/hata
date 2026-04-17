import vampytest

from ...media_item import MediaItem

from ..media_gallery import ComponentMetadataMediaGallery


def test__ComponentMetadataMediaGallery__repr():
    """
    Tests whether ``ComponentMetadataMediaGallery.__repr__`` works as intended.
    """
    items = [MediaItem('https://orindance.party/')]
    
    component_metadata = ComponentMetadataMediaGallery(
        items = items,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataMediaGallery__hash():
    """
    Tests whether ``ComponentMetadataMediaGallery.__hash__`` works as intended.
    """
    items = [MediaItem('https://orindance.party/')]
    
    component_metadata = ComponentMetadataMediaGallery(
        items = items,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def _iter_options__eq__same_type():
    items = [MediaItem('https://orindance.party/')]
    
    keyword_parameters = {
        'items': items,
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
            'items': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ComponentMetadataMediaGallery__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataMediaGallery.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    component_metadata_0 = ComponentMetadataMediaGallery(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataMediaGallery(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
