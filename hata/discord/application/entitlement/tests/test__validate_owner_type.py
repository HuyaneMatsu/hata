import vampytest

from ..fields import validate_owner_type
from ..preinstanced import EntitlementOwnerType


def _iter_options():
    yield None, EntitlementOwnerType.none
    yield EntitlementOwnerType.user, EntitlementOwnerType.user
    yield EntitlementOwnerType.user.value, EntitlementOwnerType.user


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_owner_type__passing(input_value):
    """
    Tests whether ``validate_owner_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``EntitlementOwnerType``
    """
    output = validate_owner_type(input_value)
    vampytest.assert_instance(output, EntitlementOwnerType)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with('')
def test__validate_owner_type__type_error(input_value):
    """
    Tests whether ``validate_owner_type`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value where we are expecting `TypeError`.
    
    Raises
    ------
    TypeError
    """
    validate_owner_type(input_value)
