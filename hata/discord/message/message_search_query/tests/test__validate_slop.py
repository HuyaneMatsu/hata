import vampytest

from ..constants import SLOP_DEFAULT, SLOP_MAX, SLOP_MIN
from ..fields import validate_slop


def _iter_options__passing():
    yield (
        None,
        SLOP_DEFAULT,
    )
    
    yield (
        SLOP_DEFAULT,
        SLOP_DEFAULT,
    )
    
    yield (
        1,
        1,
    )


def _iter_options__type_error():
    yield 12.6
    yield '12'


def _iter_options__value_error():
    yield SLOP_MIN - 1
    yield SLOP_MAX + 1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_slop(input_value):
    """
    Tests whether `validate_slop` works as intended.
    
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
    output = validate_slop(input_value)
    vampytest.assert_instance(output, int)
    return output
