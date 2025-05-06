import vampytest

from ...component import Component, ComponentType
from ...media_info import MediaInfo

from ..section import ComponentMetadataSection

from .test__ComponentMetadataSection__constructor import _assert_fields_set


def test__ComponentMetadataSection__from_data():
    """
    Tests whether ``ComponentMetadataSection.from_data`` works as intended.
    """
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    data = {
        'components': [component.to_data(include_internals = True) for component in components],
        'accessory': thumbnail.to_data(include_internals = True),
    }
    
    component_metadata = ComponentMetadataSection.from_data(data)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.components, tuple(components))
    vampytest.assert_eq(component_metadata.thumbnail, thumbnail)


def test__ComponentMetadataSection__to_data():
    """
    Tests whether ``ComponentMetadataSection.to_data`` works as intended.
    
    Case: include defaults and internals.
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
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'components': [component.to_data(defaults = True, include_internals = True) for component in components],
            'accessory': thumbnail.to_data(defaults = True, include_internals = True),
        },
    )
