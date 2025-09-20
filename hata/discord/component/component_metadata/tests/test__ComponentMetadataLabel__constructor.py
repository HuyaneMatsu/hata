import vampytest

from ...component import Component, ComponentType

from ..label import ComponentMetadataLabel


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataLabel`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataLabel``
        Component metadata to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataLabel)
    vampytest.assert_instance(component_metadata.component, Component, nullable = True)
    vampytest.assert_instance(component_metadata.description, str, nullable = True)
    vampytest.assert_instance(component_metadata.label, str, nullable = True)


def test__ComponentMetadataLabel__new__no_fields():
    """
    Tests whether ``ComponentMetadataLabel.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataLabel()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataLabel__new__all_fields():
    """
    Tests whether ``ComponentMetadataLabel.__new__`` works as intended.
    
    Case: all fields given.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    component_metadata = ComponentMetadataLabel(
        component = sub_component,
        description = description,
        label = label,
    )
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.component, sub_component)
    vampytest.assert_eq(component_metadata.description, description)
    vampytest.assert_eq(component_metadata.label, label)


def test__ComponentMetadataLabel__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataLabel.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataLabel.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataLabel__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataLabel.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    keyword_parameters = {
        'component': sub_component,
        'description': description,
        'label': label,
    }
    
    component_metadata = ComponentMetadataLabel.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.component, sub_component)
    vampytest.assert_eq(component_metadata.description, description)
    vampytest.assert_eq(component_metadata.label, label)
