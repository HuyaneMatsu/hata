import vampytest

from ..entity_select_default_value import EntitySelectDefaultValue
from ..preinstanced import EntitySelectDefaultValueType

from .test__EntitySelectDefaultValue__constructor import _check_are_fields_set


def test__EntitySelectDefaultValue__copy():
    """
    Tests whether ``EntitySelectDefaultValue.copy`` works as intended.
    """
    entity_id = 202310120010
    option_type = EntitySelectDefaultValueType.role
    
    entity_select_default_value = EntitySelectDefaultValue(option_type, entity_id)
    copy = entity_select_default_value.copy()
    
    _check_are_fields_set(copy)
    vampytest.assert_is_not(entity_select_default_value, copy)
    vampytest.assert_eq(entity_select_default_value, copy)


def test__EntitySelectDefaultValue__copy_with__no_fields():
    """
    Tests whether ``EntitySelectDefaultValue.copy_with`` works as intended.
    
    Case: no parameters.
    """
    entity_id = 202310120011
    option_type = EntitySelectDefaultValueType.role
    
    entity_select_default_value = EntitySelectDefaultValue(option_type, entity_id)
    copy = entity_select_default_value.copy_with()
    
    _check_are_fields_set(copy)
    vampytest.assert_is_not(entity_select_default_value, copy)
    vampytest.assert_eq(entity_select_default_value, copy)


def test__EntitySelectDefaultValue__copy_with__all_fields():
    """
    Tests whether ``EntitySelectDefaultValue.copy_with`` works as intended.
    
    Case: All field given
    """
    old_entity_id = 202310120012
    old_option_type = EntitySelectDefaultValueType.role
    
    new_entity_id = 202310120013
    new_option_type = EntitySelectDefaultValueType.channel
    
    entity_select_default_value = EntitySelectDefaultValue(old_option_type, old_entity_id)
    copy = entity_select_default_value.copy_with(entity_id = new_entity_id, option_type = new_option_type,)
    
    _check_are_fields_set(copy)
    vampytest.assert_is_not(entity_select_default_value, copy)
    vampytest.assert_eq(copy.id, new_entity_id)
    vampytest.assert_is(copy.type, new_option_type)
