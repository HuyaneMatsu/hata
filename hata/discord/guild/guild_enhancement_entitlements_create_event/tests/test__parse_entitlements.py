import vampytest

from ....application import Entitlement

from ..fields import parse_entitlements


def _iter_options():
    entitlement_id_0 = 202507050000
    entitlement_id_1 = 202507050001
    
    entitlement_0 = Entitlement.precreate(
        entitlement_id_0,
    )
    
    entitlement_1 = Entitlement.precreate(
        entitlement_id_1,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'entitlements': None,
        },
        None,
    )
    
    yield (
        {
            'entitlements': [],
        },
        None,
    )
    
    yield (
        {
            'entitlements': [
                entitlement_0.to_data(include_internals = True),
                entitlement_1.to_data(include_internals = True),
            ],
        },
        (
            entitlement_0,
            entitlement_1,
        ),
    )
    
    yield (
        {
            'entitlements': [
                entitlement_1.to_data(include_internals = True),
                entitlement_0.to_data(include_internals = True),
            ],
        },
        (
            entitlement_0,
            entitlement_1,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_entitlements(input_data):
    """
    Tests whether ``parse_entitlements`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<Entitlement>``
    """
    output = parse_entitlements(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Entitlement)
    
    return output
