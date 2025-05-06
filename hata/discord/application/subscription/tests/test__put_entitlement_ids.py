import vampytest

from ..fields import put_entitlement_ids


def _iter_options():
    entitlement_id = 202409220011
    
    yield None, False, {}
    yield None, True, {'entitlement_ids': []}
    yield (entitlement_id, ), False, {'entitlement_ids': [str(entitlement_id)]}
    yield (entitlement_id, ), True, {'entitlement_ids': [str(entitlement_id)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_entitlement_ids(input_value, defaults):
    """
    Tests whether ``put_entitlement_ids`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default values should be serialised as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_entitlement_ids(input_value, {}, defaults)
