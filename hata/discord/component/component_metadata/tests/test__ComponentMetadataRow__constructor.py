import vampytest

from ...component import Component, ComponentType

from ..row import ComponentMetadataRow


def _assert_fields_set(component_metadata):
    """
    Checks whether the given component metadata has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataRow``
        Component metadata to test.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataRow)
    vampytest.assert_instance(component_metadata.components, tuple, nullable = True)


def test__ComponentMetadataRow__new__no_fields():
    """
    Tests whether ``ComponentMetadataRow.__new__`` works as intended.
    
    Case: No fields.
    """
    component_metadata = ComponentMetadataRow()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataRow__new__all_fields():
    """
    Tests whether ``ComponentMetadataRow.__new__`` works as intended.
    
    Case: All fields.
    """
    components = [
        Component(ComponentType.button, label = 'chata'),
    ]
    
    component_metadata = ComponentMetadataRow(
        components = components,
    )
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.components, tuple(components))


def test__ComponentMetadataRow__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataRow.from_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataRow.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataRow__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataRow.from_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    components = [
        Component(ComponentType.button, label = 'chata'),
    ]
    
    keyword_parameters = {
        'components': components,
    }
    
    component_metadata = ComponentMetadataRow.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    
    vampytest.assert_eq(component_metadata.components, tuple(components))
