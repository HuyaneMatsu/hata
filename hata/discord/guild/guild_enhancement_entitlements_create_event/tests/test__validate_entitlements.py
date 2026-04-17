import vampytest

from ....application import Entitlement

from ..fields import validate_entitlements


def _iter_options__passing():
    entitlement_id_0 = 202507050004
    entitlement_id_1 = 202507050005
    
    entitlement_0 = Entitlement.precreate(
        entitlement_id_0,
    )
    entitlement_1 = Entitlement.precreate(
        entitlement_id_1,
    )
    
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            entitlement_0,
            entitlement_1,
        ],
        (
            entitlement_0,
            entitlement_1,
        ),
    )
    
    yield (
        [
            entitlement_1,
            entitlement_0,
        ],
        (
            entitlement_0,
            entitlement_1,
        ),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_entitlements(input_value):
    """
    Validates whether ``validate_entitlements`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        value to validate.
    
    Returns
    -------
    output : ``None | dict<Entitlement>``
    
    Raises
    ------
    TypeError
    """
    output = validate_entitlements(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Entitlement)
    
    return output
