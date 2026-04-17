import vampytest

from ...radio_group_option import RadioGroupOption

from ..radio_group import ComponentMetadataRadioGroup


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataRadioGroup`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataRadioGroup``
        The instance to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataRadioGroup)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.enabled, bool)
    vampytest.assert_instance(component_metadata.options, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.required, bool)


def test__ComponentMetadataRadioGroup__new__no_fields():
    """
    Tests whether ``ComponentMetadataRadioGroup.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataRadioGroup()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataRadioGroup__new__all_fields():
    """
    Tests whether ``ComponentMetadataRadioGroup.__new__`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    options = [RadioGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataRadioGroup(
        custom_id = custom_id,
        options = options,
        required = required,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.options, tuple(options))
    vampytest.assert_eq(component_metadata.required, required)


def test__ComponentMetadataRadioGroup__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataRadioGroup.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataRadioGroup.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataRadioGroup__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataRadioGroup.from_keyword_parameters`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    options = [RadioGroupOption('yume')]
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'options': options,
        'required': required,
    }
    
    component_metadata = ComponentMetadataRadioGroup.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.options, tuple(options))
    vampytest.assert_eq(component_metadata.required, required)
