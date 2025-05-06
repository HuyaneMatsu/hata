import vampytest

from ..preinstance import Preinstance


def _assert_fields_set(preinstance):
    """
    Asserts whether the given preinstance has all of its fields set.
    
    Parameters
    ----------
    preinstance : ``Preinstance``
        The preinstance to check.
    """
    vampytest.assert_instance(preinstance, Preinstance)
    vampytest.assert_instance(preinstance.keyword_parameters, dict)
    vampytest.assert_instance(preinstance.name, str)
    vampytest.assert_instance(preinstance.positional_parameters, tuple)
    vampytest.assert_instance(preinstance.value, int, str)


def test__Preinstance__new():
    """
    Tests whether ``Preinstance.__new__`` works as intended.
    """
    value = 12
    name = 'koishi'
    positional_parameters = (True, 'hell')
    keyword_parameters = {'komeiji': 'satori'}
    
    preinstance = Preinstance(
        value,
        name,
        *positional_parameters,
        **keyword_parameters,
    )
    _assert_fields_set(preinstance)
    
    vampytest.assert_eq(preinstance.value, value)
    vampytest.assert_eq(preinstance.name, name)
    vampytest.assert_eq(preinstance.positional_parameters, positional_parameters)
    vampytest.assert_eq(preinstance.keyword_parameters, keyword_parameters)


def test__Preinstance__repr():
    """
    Tests whether ``Preinstance.__repr__`` works as intended.
    """
    value = 12
    name = 'koishi'
    positional_parameters = (True, 'hell')
    keyword_parameters = {'komeiji': 'satori'}
    
    preinstance = Preinstance(
        value,
        name,
        *positional_parameters,
        **keyword_parameters,
    )
    
    output = repr(preinstance)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'{type(preinstance).__name__}(12, \'koishi\', True, \'hell\', komeiji = \'satori\')')


def test__Preinstance__hash():
    """
    Tests whether ``Preinstance.__hash__`` works as intended.
    """
    value = 12
    name = 'koishi'
    positional_parameters = (True, 'hell')
    keyword_parameters = {'komeiji': 'satori'}
    
    preinstance = Preinstance(
        value,
        name,
        *positional_parameters,
        **keyword_parameters,
    )
    
    output = hash(preinstance)
    
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    value = 12
    name = 'koishi'
    positional_parameters = (True, 'hell')
    
    keyword_parameters = {
        'komeiji': 'satori',
    }
    
    yield (
        value,
        name,
        positional_parameters,
        keyword_parameters,
        
        value,
        name,
        positional_parameters,
        keyword_parameters,
        
        True,
    )
    
    yield (
        value,
        name,
        positional_parameters,
        keyword_parameters,
        
        13,
        name,
        positional_parameters,
        keyword_parameters,
        
        False,
    )
    
    yield (
        value,
        name,
        positional_parameters,
        keyword_parameters,
        
        value,
        'orin',
        positional_parameters,
        keyword_parameters,
        
        False,
    )
    
    yield (
        value,
        name,
        positional_parameters,
        keyword_parameters,
        
        value,
        name,
        (False, 'office'),
        keyword_parameters,
        
        False,
    )
    
    
    yield (
        value,
        name,
        positional_parameters,
        keyword_parameters,
        
        value,
        name,
        positional_parameters,
        {'bird': 'brain'},
        
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Preinstance__eq(
    value_0,
    name_0,
    positional_parameters_0,
    keyword_parameters_0,
    value_1,
    name_1,
    positional_parameters_1,
    keyword_parameters_1,
):
    """
    Tests whether ``Preinstance.__eq__`` works as intended.
    
    Parameters
    ----------
    value_0 : `int | str`
        Value to create instance with.
    
    name_0 : `str`
        Name to create instance with.
    
    positional_parameters_0 : `tuple<object>`
        Positional parameter to create instance with.
    
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    value_1 : `int | str`
        Value to create instance with.
    
    name_1 : `str`
        Name to create instance with.
    
    positional_parameters_1 : `tuple<object>`
        Positional parameter to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    preinstance_0 = Preinstance(value_0, name_0, *positional_parameters_0, **keyword_parameters_0)
    preinstance_1 = Preinstance(value_1, name_1, *positional_parameters_1, **keyword_parameters_1)
    
    output = preinstance_0 == preinstance_1
    vampytest.assert_instance(output, bool)
    return output
