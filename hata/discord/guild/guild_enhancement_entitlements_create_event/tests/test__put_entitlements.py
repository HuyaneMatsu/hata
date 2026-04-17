import vampytest

from ....application import Entitlement

from ..fields import put_entitlements


def _iter_options():
    entitlement_id_0 = 202507050002
    entitlement_id_1 = 202507050003
    
    entitlement_0 = Entitlement.precreate(
        entitlement_id_0,
    )
    
    entitlement_1 = Entitlement.precreate(
        entitlement_id_1,
    )
    
    yield (
        None,
        False,
        {
            'entitlements': [],
        },
    )
    
    yield (
        None,
        True,
        {
            'entitlements': [],
        },
    )
    
    yield (
        (
            entitlement_0, 
            entitlement_1,
        ),
        False,
        {
            'entitlements': [
                entitlement_0.to_data(defaults = False, include_internals = True),
                entitlement_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        (
            entitlement_0,
            entitlement_1,
        ),
        True,
        {
            'entitlements': [
                entitlement_0.to_data(defaults = True, include_internals = True),
                entitlement_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_entitlements(input_value, defaults):
    """
    Tests whether ``put_entitlements`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<Entitlement>``
        Input value to serialize.
    
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_entitlements(input_value, {}, defaults)
