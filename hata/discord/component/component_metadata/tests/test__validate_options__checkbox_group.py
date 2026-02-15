import vampytest

from ...checkbox_group_option import CheckboxGroupOption

from ..fields import validate_options__checkbox_group


def _iter_options__passing():
    option_0 = CheckboxGroupOption('hello')
    option_1 = CheckboxGroupOption('hi')
    
    yield None, None
    yield [], None
    yield [option_0], (option_0,)
    yield [option_0, option_1], (option_0, option_1,)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_options__checkbox_group(input_value):
    """
    Tests whether ``validate_options__checkbox_group`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | tuple<CheckboxGroupOption>``
    
    Raises
    ------
    TypeError
    """
    output = validate_options__checkbox_group(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, CheckboxGroupOption)
    
    return output
