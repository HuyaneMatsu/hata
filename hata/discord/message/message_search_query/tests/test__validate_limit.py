import vampytest

from ..constants import LIMIT_DEFAULT, LIMIT_MAX, LIMIT_MIN
from ..fields import validate_limit


def _iter_options__passing():
    yield (
        None,
        LIMIT_DEFAULT,
    )
    
    yield (
        LIMIT_DEFAULT,
        LIMIT_DEFAULT,
    )
    
    yield (
        1,
        1,
    )


def _iter_options__type_error():
    yield 12.6
    yield '12'


def _iter_options__value_error():
    yield LIMIT_MIN - 1
    yield LIMIT_MAX + 1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_limit(input_value):
    """
    Tests whether `validate_limit` works as intended.
    
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
    output = validate_limit(input_value)
    vampytest.assert_instance(output, int)
    return output
