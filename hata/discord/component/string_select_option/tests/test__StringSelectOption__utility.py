import vampytest

from ....core import BUILTIN_EMOJIS

from ..string_select_option import StringSelectOption

from .test__StringSelectOption__constructor import _check_are_fields_set


def test__StringSelectOption__copy():
    """
    Tests whether ``StringSelectOption.copy`` works as intended.
    """
    value = 'last'
    label = 'night'
    emoji = BUILTIN_EMOJIS['heart']
    default = True
    description = 'good'
    
    string_select_option = StringSelectOption(value, label, emoji, default = default, description = description)
    copy = string_select_option.copy()
    
    _check_are_fields_set(copy)
    vampytest.assert_is_not(string_select_option, copy)
    vampytest.assert_eq(string_select_option.value, value)
    vampytest.assert_eq(string_select_option.label, label)
    vampytest.assert_is(string_select_option.emoji, emoji)
    vampytest.assert_eq(string_select_option.default, default)
    vampytest.assert_eq(string_select_option.description, description)


def test__StringSelectOption__copy_with__0():
    """
    Tests whether ``StringSelectOption.copy_with`` works as intended.
    
    Case: no parameters.
    """
    value = 'last'
    label = 'night'
    emoji = BUILTIN_EMOJIS['heart']
    default = True
    description = 'good'
    
    string_select_option = StringSelectOption(value, label, emoji, default = default, description = description)
    copy = string_select_option.copy_with()
    
    _check_are_fields_set(copy)
    vampytest.assert_is_not(string_select_option, copy)
    vampytest.assert_eq(copy.value, value)
    vampytest.assert_eq(copy.label, label)
    vampytest.assert_is(copy.emoji, emoji)
    vampytest.assert_eq(copy.default, default)
    vampytest.assert_eq(copy.description, description)


def test__StringSelectOption__copy_with__1():
    """
    Tests whether ``StringSelectOption.copy_with`` works as intended.
    
    Case: All field given
    """
    old_value = 'last'
    new_value = 'kono'
    old_label = 'night'
    new_label = 'chi'
    old_emoji = BUILTIN_EMOJIS['heart']
    new_emoji = BUILTIN_EMOJIS['x']
    old_default = True
    new_default = False
    old_description = 'good'
    new_description = 'shiroki'
    
    string_select_option = StringSelectOption(
        old_value, old_label, old_emoji, default = old_default, description = old_description
    )
    copy = string_select_option.copy_with(
        value = new_value,
        label = new_label,
        emoji = new_emoji,
        default = new_default,
        description = new_description,
    )
    
    _check_are_fields_set(copy)
    vampytest.assert_is_not(string_select_option, copy)
    vampytest.assert_eq(copy.value, new_value)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.default, new_default)
    vampytest.assert_eq(copy.description, new_description)
