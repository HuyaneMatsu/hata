import vampytest

from ..fields import put_sku_ids_into


def _iter_options():
    sku_id = 202409220010
    
    yield None, False, {}
    yield None, True, {'sku_ids': []}
    yield (sku_id, ), False, {'sku_ids': [str(sku_id)]}
    yield (sku_id, ), True, {'sku_ids': [str(sku_id)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_sku_ids_into(input_value, defaults):
    """
    Tests whether ``put_sku_ids_into`` is working as intended.
    
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
    return put_sku_ids_into(input_value, {}, defaults)
