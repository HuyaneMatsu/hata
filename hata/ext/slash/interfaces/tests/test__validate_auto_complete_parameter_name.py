import vampytest

from ..autocomplete import validate_auto_complete_parameter_name


def _iter_options__passing():
    yield 'koishi', 'koishi'


def _iter_options__type_error():
    yield 123.6


def _iter_options__value_error():
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_auto_complete_parameter_name(input_value):
    """
    Tests whether ``validate_auto_complete_parameter_name`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test with.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_auto_complete_parameter_name(input_value)
    vampytest.assert_instance(output, str, accept_subtypes = False)
    return output
