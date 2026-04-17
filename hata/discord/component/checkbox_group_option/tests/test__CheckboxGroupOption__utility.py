import vampytest

from ..checkbox_group_option import CheckboxGroupOption

from .test__CheckboxGroupOption__constructor import _assert_fields_set


def test__CheckboxGroupOption__copy():
    """
    Tests whether ``CheckboxGroupOption.copy`` works as intended.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    checkbox_group_option = CheckboxGroupOption(value, label, default = default, description = description)
    
    copy = checkbox_group_option.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, checkbox_group_option)
    vampytest.assert_eq(copy, checkbox_group_option)


def test__CheckboxGroupOption__copy_with__no_fields():
    """
    Tests whether ``CheckboxGroupOption.copy_with`` works as intended.
    
    Case: no fields given.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    checkbox_group_option = CheckboxGroupOption(value, label, default = default, description = description)
    
    copy = checkbox_group_option.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, checkbox_group_option)
    vampytest.assert_eq(copy, checkbox_group_option)


def test__CheckboxGroupOption__copy_with__all_fields():
    """
    Tests whether ``CheckboxGroupOption.copy_with`` works as intended.
    
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
    
    checkbox_group_option = CheckboxGroupOption(
        old_value,
        old_label,
        default = old_default,
        description = old_description
    )
    
    copy = checkbox_group_option.copy_with(
        value = new_value,
        label = new_label,
        default = new_default,
        description = new_description,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(checkbox_group_option, copy)
    
    vampytest.assert_eq(copy.value, new_value)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_eq(copy.default, new_default)
    vampytest.assert_eq(copy.description, new_description)
