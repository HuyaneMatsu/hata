import vampytest

from ..fields import validate_hang_type
from ..preinstanced import HangType


def _iter_options__passing():
    yield HangType.gaming, HangType.gaming
    yield HangType.gaming.value, HangType.gaming
    yield None, HangType.none


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_hang_type(input_value):
    """
    Tests whether ``validate_hang_type`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``HangType``
    
    Raises
    ------
    TypeError
    """
    output = validate_hang_type(input_value)
    vampytest.assert_instance(output, HangType)
    return output
