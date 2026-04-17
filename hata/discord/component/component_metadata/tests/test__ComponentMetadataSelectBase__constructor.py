import vampytest

from ..select_base import ComponentMetadataSelectBase


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataSelectBase`` has all it's attributes set.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataSelectBase)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.enabled, bool)
    vampytest.assert_instance(component_metadata.max_values, int)
    vampytest.assert_instance(component_metadata.min_values, int)
    vampytest.assert_instance(component_metadata.placeholder, str, nullable = True)
    vampytest.assert_instance(component_metadata.required, bool)


def test__ComponentMetadataSelectBase__new__no_fields():
    """
    Tests whether ``ComponentMetadataSelectBase.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataSelectBase()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataSelectBase__new__all_fields():
    """
    Tests whether ``ComponentMetadataSelectBase.__new__`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataSelectBase(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        required = required,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.required, required)


def test__ComponentMetadataSelectBase__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataSelectBase.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataSelectBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataSelectBase__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataSelectBase.from_keyword_parameters`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'required': required,
    }
    
    component_metadata = ComponentMetadataSelectBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.required, required)
