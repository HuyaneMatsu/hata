import vampytest

from ..entity_select_default_value import EntitySelectDefaultValue
from ..preinstanced import EntitySelectDefaultValueType


def test__EntitySelectDefaultValue__repr():
    """
    Tests whether ``EntitySelectDefaultValue.__repr__`` works as intended.
    """
    entity_id = 202310120006
    option_type = EntitySelectDefaultValueType.role
    
    entity_select_default_value = EntitySelectDefaultValue(option_type, entity_id)
    vampytest.assert_instance(repr(entity_select_default_value), str)


def test__EntitySelectDefaultValue__hash():
    """
    Tests whether ``EntitySelectDefaultValue.__hash__`` works as intended.
    """
    entity_id = 202310120007
    option_type = EntitySelectDefaultValueType.role
    
    entity_select_default_value = EntitySelectDefaultValue(option_type, entity_id)
    vampytest.assert_instance(hash(entity_select_default_value), int)


def test__EntitySelectDefaultValue__eq():
    """
    Tests whether ``EntitySelectDefaultValue.__eq__`` works as intended.
    """
    entity_id = 202310120008
    option_type = EntitySelectDefaultValueType.role
    
    keyword_parameters = {
        'entity_id': entity_id,
        'option_type': option_type,
    }
    
    entity_select_default_value = EntitySelectDefaultValue(**keyword_parameters)
    
    vampytest.assert_eq(entity_select_default_value, entity_select_default_value)
    vampytest.assert_ne(entity_select_default_value, object())
    
    for field_name, field_entity_id in (
        ('entity_id', 202310120009),
        ('option_type', EntitySelectDefaultValueType.channel),
    ):
        test_entity_select_default_value = EntitySelectDefaultValue(**{**keyword_parameters, field_name: field_entity_id})
        vampytest.assert_ne(entity_select_default_value, test_entity_select_default_value)
