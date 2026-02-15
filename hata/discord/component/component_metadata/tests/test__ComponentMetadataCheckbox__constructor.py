import vampytest

from ..checkbox import ComponentMetadataCheckbox


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataCheckbox`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataCheckbox``
        The instance to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataCheckbox)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.default, bool)


def test__ComponentMetadataCheckbox__new__no_fields():
    """
    Tests whether ``ComponentMetadataCheckbox.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataCheckbox()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataCheckbox__new__all_fields():
    """
    Tests whether ``ComponentMetadataCheckbox.__new__`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    default = True
    
    component_metadata = ComponentMetadataCheckbox(
        custom_id = custom_id,
        default = default,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.default, default)


def test__ComponentMetadataCheckbox__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataCheckbox.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataCheckbox.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataCheckbox__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataCheckbox.from_keyword_parameters`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    default = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'default': default,
    }
    
    component_metadata = ComponentMetadataCheckbox.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.default, default)
