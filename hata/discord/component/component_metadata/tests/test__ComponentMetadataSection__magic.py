import vampytest

from ...component import Component, ComponentType
from ...media_info import MediaInfo

from ..section import ComponentMetadataSection


def test__ComponentMetadataSection__repr():
    """
    Tests whether ``ComponentMetadataSection.__repr__`` works as intended.
    """
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component_metadata = ComponentMetadataSection(
        components = components,
        thumbnail = thumbnail,
    )
    
    output = repr(component_metadata)
    vampytest.assert_instance(output, str)


def test__ComponentMetadataSection__hash():
    """
    Tests whether ``ComponentMetadataSection.__hash__`` works as intended.
    """
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component_metadata = ComponentMetadataSection(
        components = components,
        thumbnail = thumbnail,
    )
    
    output = hash(component_metadata)
    vampytest.assert_instance(output, int)


def _iter_options__eq__same_type():
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    keyword_parameters = {
        'components': components,
        'thumbnail': thumbnail,
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
            'components': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'thumbnail': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ComponentMetadataSection__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataSection.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataSection(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataSection(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
