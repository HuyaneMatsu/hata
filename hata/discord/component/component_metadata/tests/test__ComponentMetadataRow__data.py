import vampytest

from ...component import Component, ComponentType

from ..row import ComponentMetadataRow

from .test__ComponentMetadataRow__constructor import _assert_fields_set


def test__ComponentMetadataRow__from_data():
    """
    Tests whether ``ComponentMetadataRow.from_data`` works as intended.
    """
    components = [
        Component(ComponentType.button, label = 'chata'),
    ]
    
    data = {
        'components': [component.to_data(include_internals = True) for component in components],
    }
    
    component_metadata = ComponentMetadataRow.from_data(data)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.components, tuple(components))


def test__ComponentMetadataRow__to_data():
    """
    Tests whether ``ComponentMetadataRow.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    components = [
        Component(ComponentType.button, label = 'chata'),
    ]
    
    component_metadata = ComponentMetadataRow(
        components = components,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'components': [component.to_data(defaults = True, include_internals = True) for component in components],
        },
    )
