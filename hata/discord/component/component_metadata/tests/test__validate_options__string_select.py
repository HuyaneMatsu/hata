import vampytest

from ...string_select_option import StringSelectOption

from ..fields import validate_options__string_select


def _iter_options__passing():
    option_0 = StringSelectOption('hello')
    option_1 = StringSelectOption('hi')
    
    yield None, None
    yield [], None
    yield [option_0], (option_0,)
    yield [option_0, option_1], (option_0, option_1,)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_options__string_select(input_value):
    """
    Tests whether ``validate_options__string_select`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | tuple<StringSelectOption>``
    
    Raises
    ------
    TypeError
    """
    output = validate_options__string_select(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, StringSelectOption)
    
    return output
