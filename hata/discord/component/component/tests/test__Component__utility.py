import vampytest

from ...component_metadata import ButtonStyle, TextInputStyle
from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType
from ...string_select_option import StringSelectOption

from ..component import Component
from ..preinstanced import ComponentType

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


def test__Component__cop_with__no_fields():
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


def test__Component__copy_with__fields():
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


def _iter_options__iter_components():
    component = Component(ComponentType.button, custom_id = 'chen')
    
    yield (component, [])
    yield (Component(ComponentType.row, components = [component]), [component])
    

@vampytest._(vampytest.call_from(_iter_options__iter_components()).returning_last())
def test__Component__iter_components(input_value):
    """
    Tests whether ``Component.iter_components`` works as intended.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    
    Returns
    -------
    output : list<Component>`
    """
    return [*input_value.iter_components()]


def _iter_options__iter_options():
    options = [StringSelectOption('yume')]
    
    yield (Component(ComponentType.string_select), [])
    yield (Component(ComponentType.string_select, options = options), options)


@vampytest._(vampytest.call_from(_iter_options__iter_options()).returning_last())
def test__Component__iter_options(input_value):
    """
    Tests whether ``Component.iter_options`` works as intended.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    
    Returns
    -------
    output : list<StringSelectOption>`
    """
    return [*input_value.iter_options()]


def _iter_options__iter_default_values():
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130051)]
    
    yield (Component(ComponentType.user_select), [])
    yield (Component(ComponentType.user_select, default_values = default_values), default_values)


@vampytest._(vampytest.call_from(_iter_options__iter_default_values()).returning_last())
def test__Component__iter_default_values(input_value):
    """
    Tests whether ``Component.iter_default_values`` works as intended.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    
    Returns
    -------
    output : list<EntitySelectDefaultValue>`
    """
    return [*input_value.iter_default_values()]


def _iter_options__style__read():
    yield Component(ComponentType.string_select), None
    yield Component(ComponentType.button, button_style = ButtonStyle.red), ButtonStyle.red
    yield Component(ComponentType.text_input, text_input_style = TextInputStyle.paragraph), TextInputStyle.paragraph


@vampytest._(vampytest.call_from(_iter_options__style__read()).returning_last())
def test__Component__style__read(input_value):
    """
    Tests whether ``Component.style`` works as intended.
    
    Case: reading.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    
    Returns
    -------
    output : `None | PreinstancedBase`
    """
    return input_value.style


def _iter_options__style__write():
    yield Component(ComponentType.button), ButtonStyle.red, 'button_style', ButtonStyle.red
    yield Component(ComponentType.text_input), TextInputStyle.paragraph, 'text_input_style', TextInputStyle.paragraph


@vampytest._(vampytest.call_from(_iter_options__style__write()).returning_last())
def test__Component__style__write(input_value, value, attribute_name):
    """
    Tests whether ``Component.style`` works as intended.
    
    Case: writing.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    value : ``PreinstancedBase``
        Value to set as style.
    attribute_name : `str`
        The attribute's name to read.
    
    Returns
    -------
    output : ``PreinstancedBase``
    """
    component = input_value.copy()
    component.style = value
    return getattr(component, attribute_name)
