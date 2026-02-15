import vampytest

from ..checkbox_group_option import CheckboxGroupOption


def test__CheckboxGroupOption__repr():
    """
    Tests whether ``CheckboxGroupOption.__repr__`` works as intended.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    checkbox_group_option = CheckboxGroupOption(value, label, default = default, description = description)
    
    output = repr(checkbox_group_option)
    vampytest.assert_instance(output, str)


def test__CheckboxGroupOption__hash():
    """
    Tests whether ``CheckboxGroupOption.__hash__`` works as intended.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    checkbox_group_option = CheckboxGroupOption(value, label, default = default, description = description)
    
    output = hash(checkbox_group_option)
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
def test__CheckboxGroupOption__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``CheckboxGroupOption.__eq__`` works as intended.
    
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
    checkbox_group_0 = CheckboxGroupOption(**keyword_parameters_0)
    checkbox_group_1 = CheckboxGroupOption(**keyword_parameters_1)
    
    output = checkbox_group_0 == checkbox_group_1
    vampytest.assert_instance(output, bool)
    return output
