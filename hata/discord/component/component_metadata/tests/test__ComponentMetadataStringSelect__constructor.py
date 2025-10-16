import vampytest

from ...string_select_option import StringSelectOption

from ..string_select import ComponentMetadataStringSelect


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataStringSelect`` has all it's attributes set.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataStringSelect)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.enabled, bool)
    vampytest.assert_instance(component_metadata.max_values, int)
    vampytest.assert_instance(component_metadata.min_values, int)
    vampytest.assert_instance(component_metadata.options, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.placeholder, str, nullable = True)
    vampytest.assert_instance(component_metadata.required, bool)


def test__ComponentMetadataStringSelect__new__no_fields():
    """
    Tests whether ``ComponentMetadataStringSelect.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataStringSelect()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataStringSelect__new__all_fields():
    """
    Tests whether ``ComponentMetadataStringSelect.__new__`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    options = [StringSelectOption('yume')]
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataStringSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        options = options,
        placeholder = placeholder,
        required = required,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.options, tuple(options))
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.required, required)


def test__ComponentMetadataStringSelect__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataStringSelect.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataStringSelect.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataStringSelect__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataStringSelect.from_keyword_parameters`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    options = [StringSelectOption('yume')]
    placeholder = 'swing'
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'options': options,
        'placeholder': placeholder,
        'required': required,
    }
    
    component_metadata = ComponentMetadataStringSelect.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.options, tuple(options))
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.required, required)
