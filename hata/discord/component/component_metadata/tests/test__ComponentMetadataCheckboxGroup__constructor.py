import vampytest

from ...checkbox_group_option import CheckboxGroupOption

from ..checkbox_group import ComponentMetadataCheckboxGroup


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataCheckboxGroup`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataCheckboxGroup``
        The instance to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataCheckboxGroup)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.enabled, bool)
    vampytest.assert_instance(component_metadata.max_values, int)
    vampytest.assert_instance(component_metadata.min_values, int)
    vampytest.assert_instance(component_metadata.options, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.required, bool)


def test__ComponentMetadataCheckboxGroup__new__no_fields():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataCheckboxGroup()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataCheckboxGroup__new__all_fields():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.__new__`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataCheckboxGroup(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        options = options,
        required = required,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.options, tuple(options))
    vampytest.assert_eq(component_metadata.required, required)


def test__ComponentMetadataCheckboxGroup__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataCheckboxGroup.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataCheckboxGroup__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.from_keyword_parameters`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'max_values': max_values,
        'min_values': min_values,
        'options': options,
        'required': required,
    }
    
    component_metadata = ComponentMetadataCheckboxGroup.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.options, tuple(options))
    vampytest.assert_eq(component_metadata.required, required)
