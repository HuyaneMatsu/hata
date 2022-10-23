import vampytest

from ..component import Component
from ..component_type import ComponentType

from .test__Component__constructor import _check_is_all_field_set


def test__Component__from_data():
    """
    Tests whether ``Component.from_data`` works as intended.
    """
    component_type = ComponentType.button
    custom_id = 'chen'
    
    data = {
        'type': component_type.value,
        'custom_id': custom_id,
    }
    
    component = Component.from_data(data)
    _check_is_all_field_set(component)
    vampytest.assert_is(component.type, component_type)
    vampytest.assert_is(component.custom_id, custom_id)


def test__Component__to_data():
    """
    Tests whether ``Component.to_data`` works as intended.
    
    Case: include defaults.
    """
    component_type = ComponentType.button
    custom_id = 'chen'
    
    component = Component(component_type, custom_id = custom_id)
    
    data = component.to_data(defaults = True)
    
    vampytest.assert_in('type', data)
    vampytest.assert_eq(data['type'], component_type.value)
    
    vampytest.assert_in('custom_id', data)
    vampytest.assert_eq(data['custom_id'], custom_id)
