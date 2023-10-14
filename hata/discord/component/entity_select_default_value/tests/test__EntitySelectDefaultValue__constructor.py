import vampytest

from ..entity_select_default_value import EntitySelectDefaultValue
from ..preinstanced import EntitySelectDefaultValueType


def _check_are_fields_set(entity_select_default_value):
    """
    Checks whether all attributes of the entity select default option are set.
    
    Parameters
    ----------
    entity_select_default_value : ``EntitySelectDefaultValue``
        The entity select default option to check.
    """
    vampytest.assert_instance(entity_select_default_value, EntitySelectDefaultValue)
    vampytest.assert_instance(entity_select_default_value.id, int)
    vampytest.assert_instance(entity_select_default_value.type, EntitySelectDefaultValueType)


def test__EntitySelectDefaultValue__new():
    """
    Tests whether ``EntitySelectDefaultValue.__new__`` works as intended.
    """
    entity_id = 202310120003
    option_type = EntitySelectDefaultValueType.role

    entity_select_default_value = EntitySelectDefaultValue(option_type, entity_id)
    _check_are_fields_set(entity_select_default_value)
    vampytest.assert_eq(entity_select_default_value.id, entity_id)
    vampytest.assert_is(entity_select_default_value.type, option_type)


def test__EntitySelectDefaultValue__from_fields():
    """
    Tests whether ``EntitySelectDefaultValue.from_fields`` works as intended.
    """
    entity_id = 202310120014
    option_type = EntitySelectDefaultValueType.role

    entity_select_default_value = EntitySelectDefaultValue.from_fields(option_type, entity_id)
    _check_are_fields_set(entity_select_default_value)
    vampytest.assert_eq(entity_select_default_value.id, entity_id)
    vampytest.assert_is(entity_select_default_value.type, option_type)
