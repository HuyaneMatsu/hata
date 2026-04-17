import vampytest

from ..fields import validate_flags
from ..flags import SKUFlag


def _iter_options__passing():
    yield None, SKUFlag(0)
    yield 1, SKUFlag(1)
    yield SKUFlag(1), SKUFlag(1)


def _iter_options__type_error():
    yield 'a'
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_flags(input_value):
    """
    Tests whether `validate_flags` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    value : ``SKUFlag``
    
    Raises
    ------
    TypeError
    """
    output = validate_flags(input_value)
    vampytest.assert_instance(output, SKUFlag)
    return output
