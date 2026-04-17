import vampytest

from ..checkbox import ComponentMetadataCheckbox

from .test__ComponentMetadataCheckbox__constructor import _assert_fields_set


def test__ComponentMetadataCheckbox__from_data():
    """
    Tests whether ``ComponentMetadataCheckbox.from_data`` works as intended.
    """
    custom_id = 'oriental'
    default = True
    
    data = {
        'custom_id': custom_id,
        'default': default,
    }
    
    component_metadata = ComponentMetadataCheckbox.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.default, default)


def test__ComponentMetadataCheckbox__to_data():
    """
    Tests whether ``ComponentMetadataCheckbox.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    custom_id = 'oriental'
    default = True
    
    component_metadata = ComponentMetadataCheckbox(
        custom_id = custom_id,
        default = default,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'custom_id': custom_id,
            'default': default,
        },
    )
