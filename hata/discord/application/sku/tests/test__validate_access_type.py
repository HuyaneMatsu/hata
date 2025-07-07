import vampytest

from ..fields import validate_access_type
from ..preinstanced import SKUAccessType


def _iter_options__passing():
    yield None, SKUAccessType.none
    yield SKUAccessType.full.value, SKUAccessType.full
    yield SKUAccessType.full, SKUAccessType.full


def _iter_options__type_error():
    yield 'a'
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_access_type(input_value):
    """
    Tests whether `validate_access_type` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    value : ``SKUAccessType``
    
    Raises
    ------
    TypeError
    """
    output = validate_access_type(input_value)
    vampytest.assert_instance(output, SKUAccessType)
    return output
