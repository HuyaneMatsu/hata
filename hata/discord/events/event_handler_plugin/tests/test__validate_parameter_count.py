import vampytest

from ..event import _validate_parameter_count


def _iter_options__passing():
    yield 0, 0
    yield 2, 2


def _iter_options__type_error():
    yield None
    yield object()


def _ter_options__value_error():
    yield -2


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_ter_options__value_error()).raising(ValueError))
def test__validate_parameter_count(input_value):
    """
    Tests whether ``_validate_parameter_count`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test with.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = _validate_parameter_count(input_value)
    vampytest.assert_instance(output, int)
    return output
