import vampytest

from ..fields import validate_max_values__select
from ..constants import MAX_VALUES_MAX__SELECT


def _iter_options__passing():
    yield 1, 1


def _iter_options__type_error():
    yield ''


def _iter_options__value_error():
    yield -1
    yield MAX_VALUES_MAX__SELECT + 1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_max_values__select(input_value):
    """
    Validates whether ``validate_max_values__select`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_max_values__select(input_value)
    vampytest.assert_instance(output, int)
    return output
