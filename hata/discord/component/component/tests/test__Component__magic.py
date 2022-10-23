import vampytest

from ..component import Component
from ..component_type import ComponentType


def test__Component__iter():
    """
    Tests whether ``Component.__iter__`` works as intended.
    """
    custom_id = 'chen'
    
    component = Component(ComponentType.button, custom_id = custom_id)
    
    for component, expected_output in (
        (component, []),
        (Component(ComponentType.row, components = [component]), [component]),
    ):
        output = [*component]
        vampytest.assert_eq(output, expected_output)


def test__Component__repr():
    """
    Tests whether ``Component.__repr__`` works as intended.
    """
    component_type = ComponentType.button
    
    component = Component(component_type)
    
    vampytest.assert_instance(repr(component), str)


def test__Component__hash():
    """
    Tests whether ``Component.__hash__`` works as intended.
    """
    component_type = ComponentType.button
    custom_id = 'chen'
    
    component = Component(component_type, custom_id = custom_id)
    
    vampytest.assert_instance(hash(component), int)


def test__Component__eq():
    """
    Tests whether ``Component.__eq__`` works as intended.
    """
    component_type = ComponentType.button
    custom_id = 'chen'
    
    keyword_parameters = {
        'component_type': component_type,
        'custom_id': custom_id,
    }
    
    component = Component(**keyword_parameters)
    
    vampytest.assert_eq(component, component)
    vampytest.assert_ne(component, object())
    
    for field_name, field_value in (
        ('component_type', ComponentType.user_select),
        ('custom_id', 'start'),
    ):
        test_component = Component(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component, test_component)
