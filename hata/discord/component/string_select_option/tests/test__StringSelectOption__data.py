import vampytest

from ....core import BUILTIN_EMOJIS

from ..string_select_option import StringSelectOption

from .test__StringSelectOption__constructor import _check_are_fields_set


def test__StringSelectOption__from_data():
    """
    Tests whether ``StringSelectOption.from_data`` works as intended.
    """
    value = 'last'
    label = 'night'
    emoji = BUILTIN_EMOJIS['heart']
    default = True
    description = 'good'
    
    data = {
        'value': value,
        'label': label,
        'emoji': {'name': emoji.unicode},
        'default': default,
        'description': description,
    }
    
    string_select_option = StringSelectOption.from_data(data)
    _check_are_fields_set(string_select_option)
    vampytest.assert_eq(string_select_option.value, value)
    vampytest.assert_eq(string_select_option.label, label)
    vampytest.assert_is(string_select_option.emoji, emoji)
    vampytest.assert_eq(string_select_option.default, default)
    vampytest.assert_eq(string_select_option.description, description)


def test__StringSelectOption__to_data():
    """
    Tests whether ``StringSelectOption.to_data`` works as intended.
    
    Case: include defaults
    """
    value = 'last'
    label = 'night'
    emoji = BUILTIN_EMOJIS['heart']
    default = True
    description = 'good'
    
    string_select_option = StringSelectOption(value, label, emoji, default = default, description = description)
  
    vampytest.assert_eq(
        string_select_option.to_data(
            defaults = True,
        ),
        {
            'value': value,
            'label': label,
            'emoji': {'name': emoji.unicode},
            'default': default,
            'description': description,
        },
    )
