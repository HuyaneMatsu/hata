import vampytest

from ...component import Component, ComponentType

from ..label import ComponentMetadataLabel

from .test__ComponentMetadataLabel__constructor import _assert_fields_set


def test__ComponentMetadataLabel__from_data():
    """
    Tests whether ``ComponentMetadataLabel.from_data`` works as intended.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    data = {
        'component': sub_component.to_data(defaults = True, include_internals = True),
        'description': description,
        'label': label,
    }
    
    component_metadata = ComponentMetadataLabel.from_data(data)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.component, sub_component)
    vampytest.assert_eq(component_metadata.description, description)
    vampytest.assert_eq(component_metadata.label, label)


def test__ComponentMetadataLabel__to_data():
    """
    Tests whether ``ComponentMetadataLabel.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    component_metadata = ComponentMetadataLabel(
        component = sub_component,
        description = description,
        label = label,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'component': sub_component.to_data(defaults = True, include_internals = True),
            'description': description,
            'label': label,
        },
    )
