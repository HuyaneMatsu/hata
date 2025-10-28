import vampytest

from ..attachment_input import ComponentMetadataAttachmentInput


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataAttachmentInput`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataAttachmentInput``
        The instance to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataAttachmentInput)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.max_values, int)
    vampytest.assert_instance(component_metadata.min_values, int)
    vampytest.assert_instance(component_metadata.required, bool)


def test__ComponentMetadataAttachmentInput__new__no_fields():
    """
    Tests whether ``ComponentMetadataAttachmentInput.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataAttachmentInput()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataAttachmentInput__new__all_fields():
    """
    Tests whether ``ComponentMetadataAttachmentInput.__new__`` works as intended.
    
    Case: all fields given
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
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.required, required)


def test__ComponentMetadataAttachmentInput__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataAttachmentInput.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataAttachmentInput.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataAttachmentInput__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataAttachmentInput.from_keyword_parameters`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'max_values': max_values,
        'min_values': min_values,
        'required': required,
    }
    
    component_metadata = ComponentMetadataAttachmentInput.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.required, required)
