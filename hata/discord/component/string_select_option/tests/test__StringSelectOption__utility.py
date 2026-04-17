import vampytest

from ....core import BUILTIN_EMOJIS

from ..string_select_option import StringSelectOption

from .test__StringSelectOption__constructor import _assert_fields_set


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
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, string_select_option)
    vampytest.assert_eq(copy, string_select_option)


def test__StringSelectOption__copy_with__no_fields():
    """
    Tests whether ``StringSelectOption.copy_with`` works as intended.
    
    Case: no fields given.
    """
    value = 'last'
    label = 'night'
    emoji = BUILTIN_EMOJIS['heart']
    default = True
    description = 'good'
    
    string_select_option = StringSelectOption(value, label, emoji, default = default, description = description)
    
    copy = string_select_option.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, string_select_option)
    vampytest.assert_eq(copy, string_select_option)


def test__StringSelectOption__copy_with__all_fields():
    """
    Tests whether ``StringSelectOption.copy_with`` works as intended.
    
    Case: all field given
    """
    old_value = 'last'
    old_label = 'night'
    old_emoji = BUILTIN_EMOJIS['heart']
    old_description = 'good'
    old_default = True
    
    new_value = 'kono'
    new_label = 'chi'
    new_emoji = BUILTIN_EMOJIS['x']
    new_default = False
    new_description = 'shiroki'
    
    string_select_option = StringSelectOption(
        old_value,
        old_label,
        old_emoji,
        default = old_default,
        description = old_description,
    )
    
    copy = string_select_option.copy_with(
        value = new_value,
        label = new_label,
        emoji = new_emoji,
        default = new_default,
        description = new_description,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, string_select_option)
    
    vampytest.assert_eq(copy.value, new_value)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.default, new_default)
    vampytest.assert_eq(copy.description, new_description)
