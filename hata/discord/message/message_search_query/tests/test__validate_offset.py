import vampytest

from ..constants import OFFSET_DEFAULT, OFFSET_MAX, OFFSET_MIN
from ..fields import validate_offset


def _iter_options__passing():
    yield (
        None,
        OFFSET_DEFAULT,
    )
    
    yield (
        OFFSET_DEFAULT,
        OFFSET_DEFAULT,
    )
    
    yield (
        1,
        1,
    )


def _iter_options__type_error():
    yield 12.6
    yield '12'


def _iter_options__value_error():
    yield OFFSET_MIN - 1
    yield OFFSET_MAX + 1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_offset(input_value):
    """
    Tests whether `validate_offset` works as intended.
    
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
    output = validate_offset(input_value)
    vampytest.assert_instance(output, int)
    return output
