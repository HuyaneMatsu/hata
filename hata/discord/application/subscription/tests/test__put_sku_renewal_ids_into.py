import vampytest

from ..fields import put_renewal_sku_ids


def _iter_options():
    sku_id = 202412210002
    
    yield None, False, {}
    yield None, True, {'renewal_sku_ids': []}
    yield (sku_id, ), False, {'renewal_sku_ids': [str(sku_id)]}
    yield (sku_id, ), True, {'renewal_sku_ids': [str(sku_id)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_renewal_sku_ids(input_value, defaults):
    """
    Tests whether ``put_renewal_sku_ids`` is working as intended.
    
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
    return put_renewal_sku_ids(input_value, {}, defaults)
