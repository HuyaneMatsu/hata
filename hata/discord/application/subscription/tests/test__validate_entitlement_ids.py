import vampytest

from ...entitlement import Entitlement

from ..fields import validate_entitlement_ids


def _iter_options__passing():
    entitlement_id_0 = 202409220014
    entitlement_id_1 = 202409220015
    
    entitlement_0 = Entitlement.precreate(entitlement_id_0)
    entitlement_1 = Entitlement.precreate(entitlement_id_1)
    
    yield None, None
    yield [], None
    yield [entitlement_id_0, entitlement_id_1], (entitlement_id_0, entitlement_id_1)
    yield [entitlement_id_1, entitlement_id_0], (entitlement_id_0, entitlement_id_1)
    yield [entitlement_0, entitlement_1], (entitlement_id_0, entitlement_id_1)
    yield [entitlement_1, entitlement_0], (entitlement_id_0, entitlement_id_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_entitlement_ids(input_value):
    """
    Tests whether `validate_entitlement_ids` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<int>`
    
    Raises
    ------
    TypeError
    """
    output = validate_entitlement_ids(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
