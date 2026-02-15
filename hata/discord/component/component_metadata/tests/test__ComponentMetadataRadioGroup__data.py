import vampytest

from ...radio_group_option import RadioGroupOption

from ..radio_group import ComponentMetadataRadioGroup

from .test__ComponentMetadataRadioGroup__constructor import _assert_fields_set


def test__ComponentMetadataRadioGroup__from_data():
    """
    Tests whether ``ComponentMetadataRadioGroup.from_data`` works as intended.
    """
    custom_id = 'oriental'
    options = [RadioGroupOption('yume')]
    required = True
    
    data = {
        'custom_id': custom_id,
        'options': [string_type.to_data() for string_type in options],
        'required': required,
    }
    
    component_metadata = ComponentMetadataRadioGroup.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.options, tuple(options))
    vampytest.assert_eq(component_metadata.required, required)


def test__ComponentMetadataRadioGroup__to_data():
    """
    Tests whether ``ComponentMetadataRadioGroup.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    custom_id = 'oriental'
    options = [RadioGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataRadioGroup(
        custom_id = custom_id,
        options = options,
        required = required,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'custom_id': custom_id,
            'options': [string_type.to_data(defaults = True) for string_type in options],
            'required': required,
        },
    )
