import vampytest

from ..fields import validate_type
from ..preinstanced import EntitySelectDefaultValueType


def _iter_options():
    yield None, EntitySelectDefaultValueType.none
    yield EntitySelectDefaultValueType.role, EntitySelectDefaultValueType.role
    yield EntitySelectDefaultValueType.role.value, EntitySelectDefaultValueType.role


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_type__passing(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``EntitySelectDefaultValueType``
    """
    output = validate_type(input_value)
    vampytest.assert_instance(output, EntitySelectDefaultValueType)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with(0)
def test__validate_type__type_error(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value where we are expecting `TypeError`.
    
    Raises
    ------
    TypeError
    """
    validate_type(input_value)
