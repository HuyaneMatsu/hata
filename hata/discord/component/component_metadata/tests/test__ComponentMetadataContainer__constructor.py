import vampytest

from ....color import Color

from ...component import Component, ComponentType

from ..container import ComponentMetadataContainer


def _assert_fields_set(component_metadata):
    """
    Checks whether the given component metadata has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataContainer``
        Component metadata to test.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataContainer)
    vampytest.assert_instance(component_metadata.color, Color, nullable = True)
    vampytest.assert_instance(component_metadata.components, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.spoiler, bool)


def test__ComponentMetadataContainer__new__no_fields():
    """
    Tests whether ``ComponentMetadataContainer.__new__`` works as intended.
    
    Case: No fields.
    """
    component_metadata = ComponentMetadataContainer()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataContainer__new__all_fields():
    """
    Tests whether ``ComponentMetadataContainer.__new__`` works as intended.
    
    Case: All fields.
    """
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    spoiler = True
    
    component_metadata = ComponentMetadataContainer(
        color = color,
        components = components,
        spoiler = spoiler,
    )
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.color, color)
    vampytest.assert_eq(component_metadata.components, tuple(components))
    vampytest.assert_eq(component_metadata.spoiler, spoiler)


def test__ComponentMetadataContainer__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataContainer.from_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataContainer.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataContainer__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataContainer.from_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    spoiler = True
    
    keyword_parameters = {
        'color': color,
        'components': components,
        'spoiler': spoiler,
    }
    
    component_metadata = ComponentMetadataContainer.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.color, color)
    vampytest.assert_eq(component_metadata.components, tuple(components))
    vampytest.assert_eq(component_metadata.spoiler, spoiler)
