import vampytest

from ..fields import put_sku_id


def _iter_options():
    sku_id = 202405180071

    yield 0, False, {}
    yield 0, True, {'sku_id': None}
    yield sku_id, False, {'sku_id': str(sku_id)}
    yield sku_id, True, {'sku_id': str(sku_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_sku_id(input_value, defaults):
    """
    Tests whether ``put_sku_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_sku_id(input_value, {}, defaults)
