import vampytest

from ..exceptions import SlashCommandParameterConversionError


def _assert_fields_set(exception):
    """
    Asserts whether ``SlashCommandParameterConversionError`` has every of its attributes set.
    
    Parameters
    ----------
    exception : ``SlashCommandParameterConversionError``
        The exception to test.
    """
    vampytest.assert_instance(exception, SlashCommandParameterConversionError)
    vampytest.assert_instance(exception._pretty_repr, str, nullable = True)
    vampytest.assert_instance(exception.parameter_name, str, nullable = True)
    vampytest.assert_instance(exception.received_value, str, nullable = True)
    vampytest.assert_instance(exception.excepted_type, str, nullable = True)
    vampytest.assert_instance(exception.expected_values, list, nullable = True)


def test__SlashCommandParameterConversionError__new():
    """
    Tests whether ``SlashCommandParameterConversionError.__new__`` works as intended.
    """
    parameter_name = 'hey'
    received_value = 'mister'
    excepted_type = 'int'
    expected_values = [12, 34]
    
    exception = SlashCommandParameterConversionError(
        parameter_name,
        received_value,
        excepted_type,
        expected_values,
    )
    _assert_fields_set(exception)
    
    vampytest.assert_eq(exception.parameter_name, parameter_name)
    vampytest.assert_eq(exception.received_value, received_value)
    vampytest.assert_eq(exception.excepted_type, excepted_type)
    vampytest.assert_eq(exception.expected_values, expected_values)


def _iter_options__pretty_repr():
    yield (
        ('hey', 'mister', 'int', [12, 34]),
        (
            'Parameter conversion failed\n'
            '\n'
            'Name: `hey`\n'
            'Excepted type: `int`\n'
            'Expected value(s):\n'
            '- `12`\n'
            '- `34`\n'
            'Received: `\'mister\'`'
        ),
    )
    yield (
        ('hey', 'mister', 'Channel', None),
        (
            'Parameter conversion failed\n'
            '\n'
            'Name: `hey`\n'
            'Excepted type: `Channel`\n'
            'Received: `\'mister\'`'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__pretty_repr()).returning_last())
def test__SlashCommandParameterConversionError__pretty_repr(parameters):
    """
    Tests whether ``SlashCommandParameterConversionError.pretty_repr`` works as intended.
    
    Parameters
    ----------
    parameters : `tuple<object>`
        Parameters to create the exception from.
    
    Returns
    -------
    output : `str`
    """
    exception = SlashCommandParameterConversionError(*parameters)
    
    output = exception.pretty_repr
    vampytest.assert_instance(output, str)
    return output


def test__SlashCommandParameterConversionError__repr():
    """
    Tests whether ``SlashCommandParameterConversionError.__repr__`` works as intended.
    """
    parameter_name = 'hey'
    received_value = 'mister'
    excepted_type = 'int'
    expected_values = [12, 34]
    
    exception = SlashCommandParameterConversionError(
        parameter_name,
        received_value,
        excepted_type,
        expected_values,
    )
    
    output = repr(exception)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(exception).__name__, output)
    vampytest.assert_in(f'parameter_name = {parameter_name!r}', output)
    vampytest.assert_in(f'received_value = {received_value!r}', output)
    vampytest.assert_in(f'excepted_type = {excepted_type!r}', output)
    vampytest.assert_in(f'expected_values = {expected_values!r}', output)


def _iter_options__eq__same_type():
    parameter_name = 'hey'
    received_value = 'mister'
    excepted_type = 'int'
    expected_values = [12, 34]
    yield (
        (parameter_name, received_value, excepted_type, expected_values),
        (parameter_name, received_value, excepted_type, expected_values),
        True,
    )

    yield (
        (None, received_value, excepted_type, expected_values),
        (parameter_name, received_value, excepted_type, expected_values),
        False,
    )

    yield (
        (parameter_name, None, excepted_type, expected_values),
        (parameter_name, received_value, excepted_type, expected_values),
        False,
    )
    
    yield (
        (parameter_name, received_value, None, expected_values),
        (parameter_name, received_value, excepted_type, expected_values),
        False,
    )
    
    yield (
        (parameter_name, received_value, excepted_type, None),
        (parameter_name, received_value, excepted_type, expected_values),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__SlashCommandParameterConversionError__eq__same_type(parameters_0, parameters_1):
    """
    Tests whether ``SlashCommandParameterConversionError.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    parameters_0 : `tuple<object>`
        Parameters to create exception from.
    parameters_0 : `tuple<object>`
        Parameters to create exception from.
    
    Returns
    -------
    output : `bool`
    """
    exception_0 = SlashCommandParameterConversionError(*parameters_0)
    exception_1 = SlashCommandParameterConversionError(*parameters_1)
    
    output = exception_0 == exception_1
    vampytest.assert_instance(output, bool)
    return output



def _iter_options__eq__different_type():
    yield None, False
    yield object(), False


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()).returning_last())
def test__SlashCommandParameterConversionError__eq__different_type(other):
    """
    Tests whether ``SlashCommandParameterConversionError.__eq__`` works as intended.
    
    Case: different type.
    
    Parameters
    ----------
    other : `object`
        Other object to compare the exception to.
    
    Returns
    -------
    output : `bool`
    """
    parameter_name = 'hey'
    received_value = 'mister'
    excepted_type = 'int'
    expected_values = [12, 34]
    
    exception = SlashCommandParameterConversionError(
        parameter_name,
        received_value,
        excepted_type,
        expected_values,
    )
    
    output = exception == other
    vampytest.assert_instance(output, bool)
    return output


def test__SlashCommandParameterConversionError__hash():
    """
    Tests whether ``SlashCommandParameterConversionError.__hash__`` works as intended.
    """
    parameter_name = 'hey'
    received_value = 'mister'
    excepted_type = 'int'
    expected_values = [12, 34]
    
    exception = SlashCommandParameterConversionError(
        parameter_name,
        received_value,
        excepted_type,
        expected_values,
    )
    
    output = hash(exception)
    vampytest.assert_instance(output, int)
