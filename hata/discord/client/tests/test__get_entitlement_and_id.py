import vampytest

from ...application import Entitlement

from ..request_helpers import get_entitlement_and_id


def _iter_options__passing():
    entitlement_id = 202412050050
    
    yield (
        entitlement_id,
        [],
        (None, entitlement_id),
    )
    
    
    entitlement_id = 202412050051
    
    yield (
        str(entitlement_id),
        [],
        (None, entitlement_id),
    )
    
    
    entitlement_id = 202412050052
    entitlement = Entitlement.precreate(entitlement_id) 
    
    yield (
        entitlement,
        [entitlement],
        (entitlement, entitlement_id),
    )
    
    
    entitlement_id = 202412050053
    entitlement = Entitlement.precreate(entitlement_id) 
    
    yield (
        entitlement_id,
        [entitlement],
        (entitlement, entitlement_id),
    )


def _iter_options__type_error():
    yield None, []
    yield 12.6, []


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_entitlement_and_id(input_value, extra):
    """
    Tests whether ``get_entitlement_and_id`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    extra : `list<object>`
        Extra objects to keep in cache.
    
    Returns
    -------
    output : `(None | Entitlement, int)`
    
    Raises
    ------
    TypeError
    """
    return get_entitlement_and_id(input_value)
