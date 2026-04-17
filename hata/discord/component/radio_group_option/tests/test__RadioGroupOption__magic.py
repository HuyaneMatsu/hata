import vampytest

from ..radio_group_option import RadioGroupOption


def test__RadioGroupOption__repr():
    """
    Tests whether ``RadioGroupOption.__repr__`` works as intended.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    radio_group_option = RadioGroupOption(value, label, default = default, description = description)
    
    output = repr(radio_group_option)
    vampytest.assert_instance(output, str)


def test__RadioGroupOption__hash():
    """
    Tests whether ``RadioGroupOption.__hash__`` works as intended.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    radio_group_option = RadioGroupOption(value, label, default = default, description = description)
    
    output = hash(radio_group_option)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    keyword_parameters = {
        'value': value,
        'label': label,
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
def test__RadioGroupOption__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``RadioGroupOption.__eq__`` works as intended.
    
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
    radio_group_0 = RadioGroupOption(**keyword_parameters_0)
    radio_group_1 = RadioGroupOption(**keyword_parameters_1)
    
    output = radio_group_0 == radio_group_1
    vampytest.assert_instance(output, bool)
    return output
