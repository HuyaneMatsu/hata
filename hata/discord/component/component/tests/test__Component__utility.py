import vampytest

from ...string_select_option import StringSelectOption

from ..component import Component
from ..component_type import ComponentType
from ..preinstanced import ButtonStyle, TextInputStyle

from .test__Component__constructor import _check_is_all_field_set


def test__Component__copy():
    """
    Tests whether ``Component.copy`` works as intended.
    """
    component_type = ComponentType.button
    custom_id = 'chen'
    
    component = Component(component_type, custom_id = custom_id)
    
    copy = component.copy()
    _check_is_all_field_set(copy)
    vampytest.assert_not_is(component, copy)
    vampytest.assert_is(copy.type, component_type)
    vampytest.assert_is(copy.custom_id, custom_id)


def test__Component__cop_with__0():
    """
    Tests whether ``Component.copy_with`` works as intended.
    
    Case: No fields given.
    """
    component_type = ComponentType.button
    custom_id = 'chen'
    
    component = Component(component_type, custom_id = custom_id)
    
    copy = component.copy_with()
    _check_is_all_field_set(copy)
    vampytest.assert_not_is(component, copy)
    vampytest.assert_is(copy.type, component_type)
    vampytest.assert_is(copy.custom_id, custom_id)


def test__Component__copy_with__1():
    """
    Tests whether ``Component.copy_with`` works as intended.
    
    Case: fields given.
    """
    component_type = ComponentType.button
    old_custom_id = 'chen'
    new_custom_id = 'ran'
    
    component = Component(component_type, custom_id = old_custom_id)
    
    copy = component.copy_with(custom_id = new_custom_id)
    _check_is_all_field_set(copy)
    vampytest.assert_not_is(component, copy)
    vampytest.assert_is(copy.type, component_type)
    vampytest.assert_is(copy.custom_id, new_custom_id)


def test__Component__iter_components():
    """
    Tests whether ``Component.iter_components`` works as intended.
    """
    component = Component(ComponentType.button, custom_id = 'chen')
    
    for component, expected_output in (
        (component, []),
        (Component(ComponentType.row, components = [component]), [component]),
    ):
        output = [*component.iter_components()]
        vampytest.assert_eq(output, expected_output)


def test__Component__iter_options():
    """
    Tests whether ``Component.iter_options`` works as intended.
    """
    options = [StringSelectOption('yume')]
    
    for component, expected_output in (
        (Component(ComponentType.string_select), []),
        (Component(ComponentType.string_select, options = options), options),
    ):
        output = [*component.iter_options()]
        vampytest.assert_eq(output, expected_output)



def test__Component__style__0():
    """
    Tests whether ``Component.style`` works as intended.
    
    Case: reading.
    """
    for component, expected_output in (
        (Component(ComponentType.string_select), None),
        (Component(ComponentType.button, button_style = ButtonStyle.red), ButtonStyle.red),
        (Component(ComponentType.text_input, text_input_style = TextInputStyle.paragraph), TextInputStyle.paragraph),
    ):
        vampytest.assert_is(component.style,  expected_output)


def test__Component__style__1():
    """
    Tests whether ``Component.style`` works as intended.
    
    Case: writing.
    """
    for component, value, attribute_name in (
        (Component(ComponentType.button), ButtonStyle.red, 'button_style'),
        (Component(ComponentType.text_input), TextInputStyle.paragraph, 'text_input_style'),
    ):
        component.style = value
        vampytest.assert_is(getattr(component, attribute_name), value)
