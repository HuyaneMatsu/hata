import vampytest

from ..fields import validate_flags
from ..flags import ApplicationFlag


def _iter_options__passing():
    yield None, ApplicationFlag(0)
    yield 1, ApplicationFlag(1)
    yield ApplicationFlag(1), ApplicationFlag(1)


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
        The object to validate.
    
    Returns
    -------
    value : ``ApplicationFlag``
        The validated value.
    
    Raises
    ------
    TypeError
    """
    output = validate_flags(input_value)
    vampytest.assert_instance(output, ApplicationFlag)
    return output
