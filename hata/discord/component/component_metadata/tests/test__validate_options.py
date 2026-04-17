import vampytest

from ...checkbox_group_option import CheckboxGroupOption
from ...radio_group_option import RadioGroupOption
from ...string_select_option import StringSelectOption

from ..fields import validate_options


def _iter_options__shared__passing():
    yield None, None
    yield [], None


def _iter_options__checkbox_group__passing():
    option_0 = CheckboxGroupOption('hello')
    option_1 = CheckboxGroupOption('hi')
    
    yield [option_0], (option_0,)
    yield [option_0, option_1], (option_0, option_1,)


def _iter_options__radio_group__passing():
    option_0 = RadioGroupOption('hello')
    option_1 = RadioGroupOption('hi')
    
    yield [option_0], (option_0,)
    yield [option_0, option_1], (option_0, option_1,)


def _iter_options__string_select__passing():
    option_0 = StringSelectOption('hello')
    option_1 = StringSelectOption('hi')
    
    yield [option_0], (option_0,)
    yield [option_0, option_1], (option_0, option_1,)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield [
        StringSelectOption('hello'),
        CheckboxGroupOption('hi')
    ]


@vampytest._(vampytest.call_from(_iter_options__shared__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__checkbox_group__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__radio_group__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__string_select__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_options(input_value):
    """
    Tests whether ``validate_options`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | tuple<CheckboxGroupOption> | tuple<RadioGroupOption> | tuple<StringSelectOption>``
    
    Raises
    ------
    TypeError
    """
    output = validate_options(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, CheckboxGroupOption, RadioGroupOption, StringSelectOption, )
    
    return output
