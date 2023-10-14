import vampytest

from ..entity_select_default_value import EntitySelectDefaultValue
from ..preinstanced import EntitySelectDefaultValueType

from .test__EntitySelectDefaultValue__constructor import _check_are_fields_set


def test__EntitySelectDefaultValue__from_data():
    """
    Tests whether ``EntitySelectDefaultValue.from_data`` works as intended.
    """
    entity_id = 202310120004
    option_type = EntitySelectDefaultValueType.role
    
    data = {
        'id': str(entity_id),
        'type': option_type.value,
    }
    
    entity_select_default_value = EntitySelectDefaultValue.from_data(data)
    _check_are_fields_set(entity_select_default_value)
    vampytest.assert_eq(entity_select_default_value.id, entity_id)
    vampytest.assert_is(entity_select_default_value.type, option_type)


def test__EntitySelectDefaultValue__to_data():
    """
    Tests whether ``EntitySelectDefaultValue.to_data`` works as intended.
    
    Case: include defaults
    """
    entity_id = 202310120005
    option_type = EntitySelectDefaultValueType.role
    
    entity_select_default_value = EntitySelectDefaultValue(option_type, entity_id)
  
    vampytest.assert_eq(
        entity_select_default_value.to_data(
            defaults = True,
        ),
        {
            'id': str(entity_id),
            'type': option_type.value,
        },
    )
