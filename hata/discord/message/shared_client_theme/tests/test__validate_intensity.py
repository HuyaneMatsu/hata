import vampytest

from ..constants import INTENSITY_MAX, INTENSITY_MIN
from ..fields import validate_intensity


def _iter_options__passing():
    yield (
        None,
        INTENSITY_MIN,
    )
    
    yield (
        INTENSITY_MIN,
        INTENSITY_MIN,
    )
    
    yield (
        INTENSITY_MAX,
        INTENSITY_MAX,
    )
    
    yield (
        1,
        1,
    )


def _iter_options__type_error():
    yield 12.6
    yield '12'


def _iter_options__value_error():
    yield INTENSITY_MIN - 1
    yield INTENSITY_MAX + 1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_intensity(input_value):
    """
    Tests whether `validate_intensity` works as intended.
    
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
    output = validate_intensity(input_value)
    vampytest.assert_instance(output, int)
    return output
