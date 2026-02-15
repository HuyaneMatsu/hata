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
    
    output = repr(string_select_option)
    vampytest.assert_instance(output, str)


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
    
    output = hash(string_select_option)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
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
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'value': 'orin',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'label': 'okuu',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'emoji': BUILTIN_EMOJIS['x'],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'default': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': 'satori',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__StringSelectOption__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``StringSelectOption.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    string_select_0 = StringSelectOption(**keyword_parameters_0)
    string_select_1 = StringSelectOption(**keyword_parameters_1)
    
    output = string_select_0 == string_select_1
    vampytest.assert_instance(output, bool)
    return output
