import vampytest

from ....color import Color

from ...component import Component, ComponentType

from ..container import ComponentMetadataContainer

from .test__ComponentMetadataContainer__constructor import _assert_fields_set


def test__ComponentMetadataContainer__from_data():
    """
    Tests whether ``ComponentMetadataContainer.from_data`` works as intended.
    """
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    spoiler = True
    
    data = {
        'accent_color': int(color),
        'components': [component.to_data(include_internals = True) for component in components],
        'spoiler': spoiler,
    }
    
    component_metadata = ComponentMetadataContainer.from_data(data)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.color, color)
    vampytest.assert_eq(component_metadata.components, tuple(components))


def test__ComponentMetadataContainer__to_data():
    """
    Tests whether ``ComponentMetadataContainer.to_data`` works as intended.
    
    Case: include defaults and internals.
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
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'accent_color': int(color),
            'components': [component.to_data(defaults = True, include_internals = True) for component in components],
            'spoiler': spoiler,
        },
    )
