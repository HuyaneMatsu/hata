import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..string_select_option import StringSelectOption


def _assert_fields_set(string_select_option):
    """
    Checks whether all attributes of the string select option are set.
    
    Parameters
    ----------
    string_select_option : ``StringSelectOption``
        The string select option to check.
    """
    vampytest.assert_instance(string_select_option, StringSelectOption)
    
    vampytest.assert_instance(string_select_option.default, bool)
    vampytest.assert_instance(string_select_option.description, str, nullable = True)
    vampytest.assert_instance(string_select_option.emoji, Emoji, nullable = True)
    vampytest.assert_instance(string_select_option.label, str)
    vampytest.assert_instance(string_select_option.value, str)


def test__StringSelectOption__new__no_fields():
    """
    Tests whether ``StringSelectOption`` works as intended.
    
    Case: No fields given.
    """
    value = 'last'
    
    string_select_option = StringSelectOption(value)
    _assert_fields_set(string_select_option)
    
    vampytest.assert_eq(string_select_option.value, value)
    vampytest.assert_eq(string_select_option.label, value)


def test__StringSelectOption__new__all_fields():
    """
    Tests whether ``StringSelectOption.__new__`` works as intended.
    
    Case: all fields given.
    """
    value = 'last'
    label = 'night'
    emoji = BUILTIN_EMOJIS['heart']
    default = True
    description = 'good'
    
    string_select_option = StringSelectOption(value, label, emoji, default = default, description = description)
    _assert_fields_set(string_select_option)
    
    vampytest.assert_eq(string_select_option.value, value)
    vampytest.assert_eq(string_select_option.label, label)
    vampytest.assert_is(string_select_option.emoji, emoji)
    vampytest.assert_eq(string_select_option.default, default)
    vampytest.assert_eq(string_select_option.description, description)
