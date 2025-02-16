import vampytest

from ..fields import put_id


def _iter_options():
    sku_id = 'koishi'
    yield '', False, {'id': ''}
    yield '', True, {'id': ''}
    yield sku_id, False, {'id': sku_id}
    yield sku_id, True, {'id': sku_id}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_id(input_value, defaults):
    """
    Tests whether ``put_id`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_id(input_value, {}, defaults)
