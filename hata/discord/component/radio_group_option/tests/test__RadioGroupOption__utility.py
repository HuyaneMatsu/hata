import vampytest

from ..radio_group_option import RadioGroupOption

from .test__RadioGroupOption__constructor import _assert_fields_set


def test__RadioGroupOption__copy():
    """
    Tests whether ``RadioGroupOption.copy`` works as intended.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    radio_group_option = RadioGroupOption(value, label, default = default, description = description)
    
    copy = radio_group_option.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, radio_group_option)
    vampytest.assert_eq(copy, radio_group_option)


def test__RadioGroupOption__copy_with__no_fields():
    """
    Tests whether ``RadioGroupOption.copy_with`` works as intended.
    
    Case: no fields given.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    radio_group_option = RadioGroupOption(value, label, default = default, description = description)
    
    copy = radio_group_option.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, radio_group_option)
    vampytest.assert_eq(copy, radio_group_option)


def test__RadioGroupOption__copy_with__all_fields():
    """
    Tests whether ``RadioGroupOption.copy_with`` works as intended.
    
    Case: all field given
    """
    old_value = 'last'
    old_label = 'night'
    old_default = True
    old_description = 'good'
    
    new_value = 'kono'
    new_label = 'chi'
    new_default = False
    new_description = 'shiroki'
    
    radio_group_option = RadioGroupOption(
        old_value,
        old_label,
        default = old_default,
        description = old_description
    )
    
    copy = radio_group_option.copy_with(
        value = new_value,
        label = new_label,
        default = new_default,
        description = new_description,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(radio_group_option, copy)
    
    vampytest.assert_eq(copy.value, new_value)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_eq(copy.default, new_default)
    vampytest.assert_eq(copy.description, new_description)
