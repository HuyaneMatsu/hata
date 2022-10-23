import vampytest

from ....core import BUILTIN_EMOJIS

from ..string_select_option import StringSelectOption


def test__StringSelectOption__repr():
    """
    Tests whether ``StringSelectOption.__repr__`` works as intended.
    """
    value = 'last'
    label = 'night'
    emoji = BUILTIN_EMOJIS['heart']
    default = True
    description = 'good'
    
    
    string_select_option = StringSelectOption(value, label, emoji, default = default, description = description)
    vampytest.assert_instance(repr(string_select_option), str)


def test__StringSelectOption__hash():
    """
    Tests whether ``StringSelectOption.__hash__`` works as intended.
    """
    value = 'last'
    label = 'night'
    emoji = BUILTIN_EMOJIS['heart']
    default = True
    description = 'good'
    
    
    string_select_option = StringSelectOption(value, label, emoji, default = default, description = description)
    vampytest.assert_instance(hash(string_select_option), int)


def test__StringSelectOption__eq():
    """
    Tests whether ``StringSelectOption.__eq__`` works as intended.
    """
    value = 'last'
    label = 'night'
    emoji = BUILTIN_EMOJIS['heart']
    default = True
    description = 'good'
    
    keyword_parameters = {
        'value': value,
        'label': label,
        'emoji': emoji,
        'default': default,
        'description': description,
    }
    
    string_select_option = StringSelectOption(**keyword_parameters)
    
    vampytest.assert_eq(string_select_option, string_select_option)
    vampytest.assert_ne(string_select_option, object())
    
    for field_name, field_value in (
        ('value', 'akaki'),
        ('label', 'agari'),
        ('emoji', BUILTIN_EMOJIS['x']),
        ('default', False),
        ('description', 'aka'),
    ):
        test_select_option = StringSelectOption(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(string_select_option, test_select_option)
