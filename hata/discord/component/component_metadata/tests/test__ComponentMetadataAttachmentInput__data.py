import vampytest

from ..attachment_input import ComponentMetadataAttachmentInput

from .test__ComponentMetadataAttachmentInput__constructor import _assert_fields_set


def test__ComponentMetadataAttachmentInput__from_data():
    """
    Tests whether ``ComponentMetadataAttachmentInput.from_data`` works as intended.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    data = {
        'custom_id': custom_id,
        'max_values': max_values,
        'min_values': min_values,
        'required': required,
    }
    
    component_metadata = ComponentMetadataAttachmentInput.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.required, required)


def test__ComponentMetadataAttachmentInput__to_data():
    """
    Tests whether ``ComponentMetadataAttachmentInput.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    component_metadata = ComponentMetadataAttachmentInput(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'custom_id': custom_id,
            'max_values': max_values,
            'min_values': min_values,
            'required': required,
        },
    )
