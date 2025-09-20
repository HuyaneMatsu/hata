import vampytest

from ....application_command.application_command.constants import NAME_LENGTH_MAX as APPLICATION_COMMAND_NAME_LENGTH_MAX

from ..fields import validate_application_command_name


def _iter_options__passing():
    yield None, ''
    yield '', ''
    yield 'a', 'a'
    yield 'aa', 'aa'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (APPLICATION_COMMAND_NAME_LENGTH_MAX + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_application_command_name(input_value):
    """
    Tests whether `validate_application_command_name` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_application_command_name(input_value)
    vampytest.assert_instance(output, str)
    return output
