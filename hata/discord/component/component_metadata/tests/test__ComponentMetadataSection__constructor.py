import vampytest

from ...component import Component, ComponentType
from ...media_info import MediaInfo

from ..section import ComponentMetadataSection


def _assert_fields_set(component_metadata):
    """
    Checks whether the given component metadata has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataSection``
        Component metadata to test.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataSection)
    vampytest.assert_instance(component_metadata.components, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.thumbnail, Component, nullable = True)


def test__ComponentMetadataSection__new__no_fields():
    """
    Tests whether ``ComponentMetadataSection.__new__`` works as intended.
    
    Case: No fields.
    """
    component_metadata = ComponentMetadataSection()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataSection__new__all_fields():
    """
    Tests whether ``ComponentMetadataSection.__new__`` works as intended.
    
    Case: All fields.
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
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.components, tuple(components))
    vampytest.assert_eq(component_metadata.thumbnail, thumbnail)


def test__ComponentMetadataSection__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataSection.from_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataSection.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataSection__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataSection.from_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
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
    
    component_metadata = ComponentMetadataSection.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.components, tuple(components))
    vampytest.assert_eq(component_metadata.thumbnail, thumbnail)
