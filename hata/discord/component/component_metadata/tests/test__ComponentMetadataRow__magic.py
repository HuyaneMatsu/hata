import vampytest

from ...component import Component, ComponentType

from ..row import ComponentMetadataRow


def test__ComponentMetadataRow__repr():
    """
    Tests whether ``ComponentMetadataRow.__repr__`` works as intended.
    """
    components = [Component(ComponentType.button, label = 'chata')]
    
    component_metadata = ComponentMetadataRow(
        components = components,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataRow__hash():
    """
    Tests whether ``ComponentMetadataRow.__hash__`` works as intended.
    """
    components = [Component(ComponentType.button, label = 'chata')]
    
    component_metadata = ComponentMetadataRow(
        components = components,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataRow__eq():
    """
    Tests whether ``ComponentMetadataRow.__eq__`` works as intended.
    """
    components = [Component(ComponentType.button, label = 'chata')]
    
    keyword_parameters = {
        'components': components,
    }
    
    component_metadata = ComponentMetadataRow(**keyword_parameters)
    
    vampytest.assert_eq(component_metadata, component_metadata)
    vampytest.assert_ne(component_metadata, object())

    for field_name, field_value in (
        ('components', None),
    ):
        test_component_metadata = ComponentMetadataRow(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)
