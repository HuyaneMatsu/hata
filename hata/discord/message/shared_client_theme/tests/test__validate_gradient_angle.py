import vampytest

from ..constants import GRADIENT_ANGLE_MAX, GRADIENT_ANGLE_MIN
from ..fields import validate_gradient_angle


def _iter_options__passing():
    yield (
        None,
        GRADIENT_ANGLE_MIN,
    )
    
    yield (
        GRADIENT_ANGLE_MIN,
        GRADIENT_ANGLE_MIN,
    )
    
    yield (
        GRADIENT_ANGLE_MAX,
        GRADIENT_ANGLE_MAX,
    )
    
    yield (
        1,
        1,
    )


def _iter_options__type_error():
    yield 12.6
    yield '12'


def _iter_options__value_error():
    yield GRADIENT_ANGLE_MIN - 1
    yield GRADIENT_ANGLE_MAX + 1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_gradient_angle(input_value):
    """
    Tests whether `validate_gradient_angle` works as intended.
    
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
    output = validate_gradient_angle(input_value)
    vampytest.assert_instance(output, int)
    return output
