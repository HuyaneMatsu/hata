import vampytest

from ..fields import validate_access_type
from ..preinstanced import SKUAccessType


def _iter_options():
    yield None, SKUAccessType.none
    yield SKUAccessType.full, SKUAccessType.full
    yield SKUAccessType.full.value, SKUAccessType.full


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_access_type__passing(input_value):
    """
    Tests whether ``validate_access_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``SKUAccessType``
    """
    output = validate_access_type(input_value)
    vampytest.assert_instance(output, SKUAccessType)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with('')
def test__validate_access_type__type_error(input_value):
    """
    Tests whether ``validate_access_type`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value where we are expecting `TypeError`.
    
    Raises
    ------
    TypeError
    """
    validate_access_type(input_value)
