import vampytest

from ....application import Entitlement

from ..fields import validate_entitlements


def _iter_options():
    entitlement_id_0 = 202310050006
    entitlement_id_1 = 202310050007
    
    entitlement_0 = Entitlement.precreate(entitlement_id_0)
    entitlement_1 = Entitlement.precreate(entitlement_id_1)

    yield (None, None)
    yield ([], None)
    yield ([entitlement_0], (entitlement_0,))
    yield ([entitlement_1, entitlement_0], (entitlement_0, entitlement_1))


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_entitlements__passing(input_value):
    """
    Validates whether ``validate_entitlements`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<Entitlement>`
    """
    return validate_entitlements(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_entitlements__type_error(input_value):
    """
    Validates whether ``validate_entitlements`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_entitlements(input_value)
