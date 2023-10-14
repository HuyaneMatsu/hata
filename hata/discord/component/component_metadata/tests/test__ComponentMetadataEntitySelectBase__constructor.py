import vampytest

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..entity_select_base import ComponentMetadataEntitySelectBase


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataEntitySelectBase`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataEntitySelectBase``
        Component metadata to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataEntitySelectBase)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.enabled, bool)
    vampytest.assert_instance(component_metadata.max_values, int)
    vampytest.assert_instance(component_metadata.min_values, int)
    vampytest.assert_instance(component_metadata.placeholder, str, nullable = True)
    vampytest.assert_instance(component_metadata.default_values, tuple, nullable = True)


def test__ComponentMetadataEntitySelectBase__new__no_fields():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataEntitySelectBase()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataEntitySelectBase__new__all_fields():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.__new__`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140000)]
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        default_values = default_values,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.default_values, tuple(default_values))


def test__ComponentMetadataEntitySelectBase__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataEntitySelectBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataEntitySelectBase__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.from_keyword_parameters`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140001)]
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'default_values': default_values,
    }
    
    component_metadata = ComponentMetadataEntitySelectBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.default_values, tuple(default_values))
